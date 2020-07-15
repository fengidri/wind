#encoding:utf8

import vim
import os
import pyvim
import sys
from pyvim import log as logging
from frainui import Search
import libtag

class g:
    last_path = None
    last_pos  = None
    last_tag  = None

def encode(cmd):
    # 把 tags 文件的里 命令式 tag 进行转码
    show_enco=vim.eval('&encoding')
    file_enco=vim.eval('&fileencoding')
    if file_enco != show_enco:
        if file_enco:
            cmd = cmd.decode(file_enco).encode(show_enco)
    return cmd



def goto_file(path):
    if path == vim.current.buffer.name:
        return

    vim.command('update')

    for b in vim.buffers:
        if path == b.name:
            vim.current.buffer = b
            break
    else:
        vim.command('silent edit %s'  % path)



class TagStack(object):
    stacks = {}
    stack = None
    def __new__(cls, *args, **kwargs):
        w = vim.current.window
        stack = cls.stacks.get(w)
        if not stack:
            org = super(TagStack, cls)
            stack = org.__new__(cls, *args, **kwargs)
            cls.stacks[w] = stack
        return stack

    def __init__(self):
        if None == self.stack:
            self.stack = []

    def push(self, frame):
        self.stack.append(frame)

    def pop(self):
        if not self.stack:
            return
        return self.stack.pop()


# d  macro definitions
# e  enumerators (values inside an enumeration)
# f  function definitions
# g  enumeration names
# h  included header files
# l  local variables [off]
# m  struct, and union members
# p  function prototypes [off]
# s  structure names
# t  typedefs
# u  union names
# v  variable definitions
# x  external and forward variable declarations [off]
# z  function parameters inside function definitions [off]
# L  goto labels [off]
# D  parameters inside macro definitions [off]

class TagOne(object):
    def __init__(self, line):
        self.msg_guess_cursor = False
        self.show = None
        self.pattern = None

        if ';"' in line:
            t = line.split('\t', 2)

            self.tag = t[0]
            self.file_path = t[1]

            pos = t[2].find(';"\t')

            pattern = t[2][0:pos]

            if pattern.isdigit():
                pattern = int(pattern) - 1
                self.line_nu = pattern
            else:
                pattern = pattern[2:-2]
                pattern = pattern.replace('\\t', '\t').replace('\\/', '/')
                pattern = pattern.replace(r'\r','')
                #pattern = encode(pattern)
            self.pattern = pattern

            t = t[2][pos:].split('\t')

            kind_map = {'p':'prototype',
                    'f': 'function',
                    'm': 'member',
                    's': 'struct',
                    'v': 'variable',
                    'd': 'marco',
                    'e': 'enumerator',
                    }
            self.kind = kind_map.get(t[1], self.kind)
        else: # xref
            t = line.split(None, 4)
            self.tag = t[0]
            self.kind = t[1]
            self.file_path = t[3]
            self.line_nu = int(t[2]) - 1
            self.show = t[4]


    def goto(self):
        self.last_file = vim.current.buffer.name
        self.last_cursor = vim.current.window.cursor
        return self._goto()

    def _goto(self):
        g.last_pos = None
        g.last_path = None
        g.last_tag = self.tag

        tag = self.tag

        msg = ''

        root = pyvim.get_cur_root()
        path = os.path.join(root, self.file_path)
        #logging.error('goto path: %s, %s, %s, %s' %(path, pattern, tag, pos))

        goto_file(path)

        pattern = self.pattern
        pattern_nu = None
        if self.line_nu:
            pattern_nu = self.line_nu
        else:
            pattern_nu_b = None
            for i, l in enumerate(vim.current.buffer):
                if l == pattern:
                    pattern_nu = i
                    break

                if l.find(tag) > -1 and None == pattern_nu_b:
                    pattern_nu_b  = i
                    logging.error('suspicious pattern(%s): %s: %s', tag, l, pattern)

            else:
                msg = "linue num is guessed"
                pattern_nu  = pattern_nu_b


        if pattern_nu == None:
            return 'error patten: %s' % pattern

        pattern = vim.current.buffer[pattern_nu]
        col_nu = pattern.find(tag)
        if col_nu < 0:
            col_nu = 0

        pos = (pattern_nu + 1, col_nu)

        vim.current.window.cursor = pos
        g.last_pos = pos
        g.last_path = path

        try:
    #        vim.command('%foldopen!')
            vim.command('normal zz')
        except vim.error as e:
            logging.error(e)

        return msg

    def back(self):
        goto_file(self.last_file)

        vim.current.window.cursor = self.last_cursor

        try:
#            vim.command('%foldopen!')
            vim.command('normal zz')
        except vim.error as e:
            logging.error(e)


class TagFrame(object):
    def __init__(self, lines):
        self.kinds = {}
        taglist   = []

        for line in lines:
            tag = TagOne(line)

            if isinstance(tag.pattern, str):
                " skip EXPORT_SYMBOL inside kernel source"
                if tag.pattern.startswith('EXPORT_SYMBOL'):
                    continue

            if self.kinds.get(tag.kind):
                self.kinds[tag.kind] += 1
            else:
                self.kinds[tag.kind] = 1

            taglist.append(tag)

        taglist = self.sort(taglist)

        self.taglist   = taglist
        self.tagname   = taglist[0].tag
        self.num       = len(self.taglist)

    def sort(self, taglist):
        "同一个 tag 的多个纪录, 把 f, v kind 的放前面."

        _taglist = []

        #kinds = 'fstudvm'
        kinds = ['function', 'struct', 'marco', 'variable', 'member']
        for k in kinds:
            for tag in taglist:
                if tag.kind == k:
                    _taglist.append(tag)

        for tag in taglist:
            if tag.kind in kinds:
                continue
            _taglist.append(tag)

        return _taglist

    def _goto(self, index):
        tag  = self.taglist[index]

        msg = tag.goto()
        TagStack().push(tag)

        pyvim.echoline('Tag(%s) goto %s/%s kind: %s. [%s]' %
                (tag.tag, index + 1, self.num, tag.kind, msg))

    def ui_select(self):
        '使用 frainui 展示, 用户进行选择'

        lines = []
        maxlen = 0
        for t in self.taglist:
            l = len(t.file_path)
            if l > maxlen:
                maxlen = l

        for t in self.taglist:
            f = t.file_path

            if t.show:
                l = t.show
            else:
                l = t.pattern

            if isinstance(l, str):
                l = l.strip()

            tt = r"%s  %s|%s" % (f.ljust(maxlen), t.kind[0:3], l)
            line = encode(tt)
            lines.append(line)

        win = Search(lines)
        win.FREventBind('Search-Quit', self.quit_search)

    def goto_p(self):
        if self.tagname != g.last_tag:
            return

        kind = 'prototype'

        if self.kinds.get(kind, 0) == 0:
            return

        if g.last_path != vim.current.buffer.name:
            return

        if not g.last_pos:
            return

        if g.last_pos[0] != vim.current.window.cursor[0]:
            return

        if 1 < self.kinds.get(kind):
            self.ui_select()
            return True

        for i, tag in enumerate(self.taglist):
            if tag.kind == kind:
                self._goto(i)
                return True


    def goto(self, index = None):
        '不指定的情况下, 并且只一个纪录直接跳转'
        if self.num < 2:
            index = 0

        if None != index:
            self._goto(index)
            return

        '如果有对应的申明 p, 并且当前还在上一次跳转之后的地方. 尝试去申明'
        if self.goto_p():
            return

        '如果不算 p(申明) 只有一个, 直接跳转到另一个'
        if self.num - self.kinds.get('prototype', 0) == 1:
            for i, tag in enumerate(self.taglist):
                if tag.kind == 'prototype':
                    continue
                self._goto(i)
                return

        self.ui_select()


    def quit_search(self, win, index):
        logging.error("tags search window get: %s", index)

        if index == None:
            return

        if index > -1:
            self._goto(index)


@pyvim.cmd()
def Tag(tag = None):
    if not tag:
        tag = pyvim.current_word()

    root = pyvim.get_cur_root()
    if not root:
        pyvim.echoline('not in project path')
        return

    taglist, err = libtag.find_tag(root, tag)
    if not taglist:
        pyvim.echoline(err)
        return

    frame = TagFrame(taglist)

    frame.goto()

@pyvim.cmd()
def TagBack():
    stack = TagStack()

    tag = stack.pop()

    if not tag:
        vim.command(" echo 'there is no tag in stack'")
        return 0

    tag.back()

@pyvim.cmd()
def TagRefresh():
    root = pyvim.get_cur_root()

    libtag.refresh(root)

    vim.command("echo 'the ctags is ok'")


@pyvim.cmd()
def TagKernel():
    libtag.g.iskernel = True;
    TagRefresh()
