#encoding:utf8

import vim
import os
import pyvim
import sys
from pyvim import log as logging
from frainui import Search
import libtag

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



def goto(path, pattern, tag, pos):
    msg = ''

    root = pyvim.get_cur_root()
    path = os.path.join(root, path)
    logging.error('goto path: %s, %s, %s, %s' %(path, pattern, tag, pos))

    goto_file(path)


    pattern_nu = None
    if isinstance(pattern, str):
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

    else:
        pattern_nu  = pattern

    if pattern_nu != None:
        pattern = vim.current.buffer[pattern_nu]
        col_nu = pattern.find(tag)
        if col_nu < 0:
            col_nu = 0

        pos = (pattern_nu + 1, col_nu)
    else:
        return 'error patten: '+pattern

    vim.current.window.cursor = pos

    try:
#        vim.command('%foldopen!')
        vim.command('normal zz')
    except vim.error as e:
        logging.error(e)

    return msg




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


class TagOne(object):
    def __init__(self, line):
        self.msg_guess_cursor = False

        t = line.split('\t', 2)

        self.tag = t[0]
        self.file_path = t[1]

        pos = t[2].find(';"\t')

        pattern = t[2][0:pos]

        if pattern.isdigit():
            pattern = int(pattern) - 1
        else:
            pattern = pattern[2:-2]
            pattern = pattern.replace('\\t', '\t').replace('\\/', '/')
            pattern = pattern.replace(r'\r','')
            #pattern = encode(pattern)
        self.pattern = pattern

        t = t[2][pos:].split('\t')
        self.kind      = t[1]


    def goto(self):
        self.last_file = vim.current.buffer.name
        self.last_cursor = vim.current.window.cursor
        return goto(self.file_path, self.pattern, self.tag, None)

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

        _taglist = []

        "同一个 tag 的多个纪录, 把 f, v kind 的放前面."
        for tag in taglist:
            if tag.kind == 'f' or tag.kind == 'v':
                _taglist.append(tag)
                continue

        for tag in taglist:
            if tag.kind == 'f' or tag.kind == 'v':
                continue
            _taglist.append(tag)


        self.taglist   = _taglist
        self.tagname   = taglist[0].tag
        self.num       = len(self.taglist)

    def _goto(self, index):
        tag  = self.taglist[index]


        msg = tag.goto()
        TagStack().push(tag)

        pyvim.echoline('Tag(%s) goto %s/%s kind: %s. [%s]' %
                (tag.tag, index + 1, self.num, tag.kind, msg))

    def goto(self, index = None):
        '不指定的情况下, 并且只一个纪录直接跳转'
        if self.num < 2:
            index = 0

        if None != index:
            self._goto(index)
            return

        '如果不算 p(申明) 只有一个, 直接跳转到另一个上面'
        if self.num - self.kinds.get('p', 0) == 1:
            for i, tag in enumerate(self.taglist):
                if tag.kind == 'p':
                    continue
                self._goto(i)
                return


        '使用 frainui 展示, 用户进行选择'

        lines = []
        maxlen = 0
        for t in self.taglist:
            l = len(t.file_path)
            if l > maxlen:
                maxlen = l

        for t in self.taglist:
            f = t.file_path
            l = t.pattern
            if isinstance(l, str):
                l = l.strip()

            tt = r"%s  %s|%s" % (f.ljust(maxlen), t.kind, l)
            line = encode(tt)
            lines.append(line)

        win = Search(lines)
        win.FREventBind('Search-Quit', self.quit_search)

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



