#encoding:utf8



import vim
import os
import pyvim
import ctags
import sys
from pyvim import log as logging
from frainui import Search


def encode(cmd):
    # 把 tags 文件的里 命令式 tag 进行转码
    show_enco=vim.eval('&encoding')
    file_enco=vim.eval('&fileencoding')
    if file_enco != show_enco:
        if file_enco:
            cmd = cmd.decode(file_enco).encode(show_enco)
    return cmd


def goto(path, prefix, pos):

    logging.error('goto path: %s, %s, %s' %(path, prefix, pos))

    if path != vim.current.buffer.name:
        vim.command('update')

        for b in vim.buffers:
            if path == b.name:
                vim.current.buffer = b
                break
        else:
            vim.command('silent edit %s'  % path)

    if prefix:
        line = prefix[0]
        tagname = prefix[1]

        line_nu = None
        if isinstance(line, str):
            for i, l in enumerate(vim.current.buffer):
                if l.startswith(line[2:-1]):
                    line_nu = i
        else:
            line_nu = line

        if line_nu != None:
            line = vim.current.buffer[line_nu]
            col_nu = line.find(tagname)
            if col_nu < 0:
                col_nu = 0

            pos = (line_nu + 1, col_nu)
        else:
            logging.error('patten: '+line)
            return

    vim.current.window.cursor = pos

    try:
#        vim.command('%foldopen!')
        vim.command('normal zz')
    except vim.error as e:
        logging.error(e)


class Frame(object):
    def __init__(self, taglist):
        self.taglist   = taglist
        self.tagname   = taglist[0].tag
        self.num       = len(self.taglist)
        self.index     = 0
        self.file_path = pyvim.filepath()
        self.cursor    = vim.current.window.cursor

    def goto(self):
        goto(self.file_path, None, self.cursor)


class Tag(object):
    def __init__(self, root, entry):
        self.tag = entry[b"name"]

        root = bytes(root, encoding="utf-8")

        self.file_path = os.path.join(root, entry[b"file"])

        line = entry[b"pattern"]
        if line.isdigit():
            self.line = int(line) - 1
        else:
            line = str(line)
            patten = line.replace(r'\/', '/')
            patten = patten.replace(r'\r','')
            self.line = encode(patten[2:-2])

        self.line_num = entry[b"lineNumber"]
        self.kind = entry[b"kind"]

    def goto(self):
        goto(self.file_path.decode('utf8'),
                (self.line, self.tag.decode('utf8')), None)



class TagList:
    tagsfile = ''
    list_tags = []
    def __init__(self, root_dir):
        self.tagfile = None
        self.tag_root_dir = root_dir
        self.open()

    def open(self):
        tags = os.path.join(self.tag_root_dir, '.tags')
        if not os.path.isfile(tags):
            tags = os.path.join(self.tag_root_dir, 'tags')
            if not os.path.isfile(tags):
                logging.error("not found the tags/.tags file in %s.",
                        self.tag_root_dir)
                return False

        self.items = None
        self.funs = None

        self.tagsfile = tags;
        self.tagfile = ctags.CTags(bytes(self.tagsfile, encoding='utf-8'))
        self.entry = ctags.TagEntry()
        return True

    def refresh( self ):
        if self.tag_root_dir:
            os.popen("cd %s;ctags -f .tags -R *"  % self.tag_root_dir )
            vim.command("echo 'the ctags is ok'")
            self.open( )
        else:
            logging.error("this is not a project" )

    def get_items( self ):
        if self.items == None:

            items = [  ]
            status = self.tagfile.find(self.entry, '', ctags.TAG_PARTIALMATCH )
            while ( status ):
                items.append( self.entry["name"] )
                status = self.tagfile.findNext(self.entry)
            self.items = items
        return self.items

    def get_funs( self ):
        if self.funs == None:

            funs = [  ]
            status = self.tagfile.find(self.entry, '', ctags.TAG_PARTIALMATCH )
            while ( status ):
                if self.entry[ "kind" ] == 'f':
                    funs.append( self.entry["name"] )
                status = self.tagfile.findNext(self.entry)
            self.funs = funs
        return list(set(self.funs ))

    def out_list(self, tag, MODE=ctags.TAG_FULLMATCH):
        "输出关于tag的所有信息"
        if not self.tagfile:
            self.open( )
            if self.tagfile == None:
                vim.command( "echo 'no tagfile'")
                return None

        list_tags = []
        status = self.tagfile.find(self.entry, bytes(tag, encoding='utf-8'), MODE )
        if not status:
            return None

        while (status):
            list_tags.append(Tag(self.tag_root_dir, self.entry))
            status = self.tagfile.findNext(self.entry)
        return list_tags




class class_tag:
    wstacks = { }
    last_tag = ''
    def __init__(self):
        self.tagsfile_list = []
        for path in pyvim.Roots:
            self.tagsfile_list.append(TagList(path))

    def wstack(self):
        "每一个窗口都有一个对应的stack,以及一些传回信息"
        w = vim.current.window
        stack = self.wstacks.get(w)
        if not stack :
            stack = []
            self.wstacks[w] = stack
        return stack

    def wstack_push(self, frame):
        "在当前窗口的stack后加上新tag的信息"
        stack = self.wstack()

        stack.append(frame)

    def wstack_pop(self):
        stack = self.wstack()
        if stack:
            return stack.pop()
        return None

    ############################################################################

    def find_tag(self, tag):
        if not self.tagsfile_list:
            logging.error('this is not a project context')
            return 0

        wstack = TAG.wstack()
        if wstack and tag == wstack[-1].tagname:
            #相同的tag  平行跳转
            return True

        taglist = None
        for tagsfile in self.tagsfile_list:
            taglist = tagsfile.out_list(tag)
            if taglist:
                break

        if not taglist:
            return 0

        frame = Frame(taglist)

        "加入到stack中tag从定义处开始"
        for pos, taginfos in enumerate(taglist):
            if taginfos.kind == 'function':
                break
            if taginfos.kind  == 'variable':
                break

        frame.index = pos

        #加入到stack中去
        self.wstack_push(frame)
        return True

    def jump_tag(self):
        frame = self.wstack()[-1]

        if frame.num == 0:
            vim.command("echo 'not find'")
            return 0

        #echo
        #cmd = "echo '%s %s %s/%s'"  % ( frame.tagname,
        #    frame.taglist[frame.index].kind,
        #    frame.index, frame.num)

        #print(cmd)
        #vim.command(cmd)

        self.goto(frame)

        frame.index += 1
        if frame.index >= frame.num:
            frame.index  = 0

    def goto(self, frame):
        if frame.num < 4:
            frame.taglist[frame.index].goto()
        else:
            lines = []
            maxlen = 0
            for t in frame.taglist:
                l = len(os.path.basename(t.file_path))
                if l > maxlen:
                    maxlen = l

            for t in frame.taglist:
                f = os.path.basename(t.file_path)
                l = t.line
                if isinstance(l, basestring):
                    l = l.strip()
                tt = r"%s  %s" % (f.ljust(maxlen), l)
                line = encode(tt)
                lines.append(line)

            win = Search(lines)
            win.FREventBind('Search-Quit', self.quit_search)

    def quit_search(self, win, index):
        logging.error("tags search window get: %s", index)

        if index > -1:
            frame = self.wstack()[-1]

            frame.taglist[index].goto()
            frame.index = index


@pyvim.cmd()
def TagJump(tag = None):
    global TAG
    if TAG == None:
        TAG = class_tag()

    if not tag:
        tag = pyvim.current_word()

    if TAG.find_tag(tag):
        TAG.jump_tag()

    try:
        vim.command('normal zz')
    except vim.error as e:
        logging.error(e)

@pyvim.cmd()
def TagBack():
    if TAG == None:
        return

    frame = TAG.wstack().pop()
    if not frame:
        vim.command(" echo 'there is no tag in stack'")
        return 0

    if not os.path.isfile(frame.file_path):
        return

    frame.goto()

@pyvim.cmd()
def TagRefresh():
    global TAG
    if TAG == None:
        return

    for tagfile in TAG.tagsfile_list:
        tagfile.refresh( )


if not __name__== "__main__":
    TAG = None

