# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import os
import logging
log = logging.getLogger("wind")

import event

Roots = [] # 当前在编辑中的文件的根目录


# for previous
__previous = None
def previous():
    return __previous

@event.event("WinLeave")
def _previous():
    global __previous
    __previous = vim.current.window


# 记录窗口跳转的过程
#class WStack(dict):
#    def __init__(self):
#        pass
#
#
#    def append(self):
#        bn = vim.current.buffer.number
#        cursor = vim.current.window.cursor
#
#        pos = (bn, cursor)
#
#        stack = self.get(vim.current.window)
#        if not stack:
#            self[vim.current.window] = [pos]
#        else:
#            stack.append(pos)
#
#    def pop(self, pos):
#        stack = self.get(vim.current.window)
#        if not stack:
#            return
#        else:
#            return stack.pop()

def parse_tags(lines):
    tags = {}
    for line in lines:
        if line[0] == '!':
            continue
        tt = line.split('\t', 2)
        if not tt:
            continue

        o = tt[-1]

        tagname = tt[0]
        tagfile = tt[1]
        pos = o.find(';"')
        if pos == -1:
            cmd = o
            ext = None
        else:
            cmd = o[0: pos]
            ext = o[pos + 2:].strip().split('\t')

        if cmd.isdigit():
            cmd = int(cmd)
        else:
            cmd = o[2: -2]

        if tags.get(tagname):
            tags[tagname].append((tagfile, cmd, ext))
        else:
            tags[tagname] = [(tagfile, cmd, ext)]

    return tags

def get_cur_root(): # 返回当前文件所在的 root
    cur_paths = vim.current.buffer.name
    for path in pyvim.Roots:
        if cur_paths.startswith( path ):
            return path


def settitle(name):#设置vim 窗口的title
    # 如果没有设置name, 则使用第一个root的name
    vim_title = name.replace( ' ', '\\ ')
    if os.environ.get('TMUX'):
        cmd = "tmux rename-window '%s'" % vim_title
        os.system(cmd)
    else:
        cmd =  "set title titlestring=%s" % vim_title
        vim.command(cmd)
    log.error('Set Title: %s' % cmd)

def gettitle():
    if os.environ.get('TMUX'):
        cmd = "tmux display-message -p '#W'"
        return os.popen(cmd).read().strip()
    else:
        return ''



def origin_win( ):
    vim.command( "wincmd p")

def win_max( ):
    vim.command( "set lines=999" )
    vim.command( "set columns=999")


"get last select text"
def select():
    ((line1, col1), (line2, col2)) = selectpos()

    tmp = []
    for i in range(line1, line2  + 1):
        line = vim.current.buffer[i]
        s = 0
        e = len(line) - 1

        if i == line1:
            s = col1

        if i == line2:
            e = col2

        tmp.append(line[s: e + 1])
    return '\n'.join(tmp)

def selectpos():
    line1 = int(vim.eval("line(\"'<\")")) - 1
    line2 = int(vim.eval("line(\"'>\")")) - 1
    col1  = int(vim.eval("col(\"'<\")"))  - 1
    col2  = int(vim.eval("col(\"'>\")"))  - 1
    return ((line1, col1), (line2, col2))



"动作: 打开一个窗口. 在这个窗口中显示输出信息"
class vstdout( object ):
    def __init__( self, title=None ):
        if title == None:
            title = ">>>Vim Stdout.<<<"
        self.save_w = vim.current.window
        vim.command( "botright new ")
        vim.command( "set buftype=nofile" )
        vim.command( "set ft=vstdout")

        self.buf = vim.current.buffer
        self.buf[ 0 ] = title
        self.stdout_w = vim.current.window

    def write( self, line):
        line = line.replace( '\n', '' )
        self.buf.append( line )

    def flush( self ):
        pass

    def close( self ):
        vim.current.window = self.stdout_w
        vim.command( "close" )
        vim.current.window = self.save_w



def getchr():#getchr
    ch=vim.eval("getchar()")
    if ch == '\x80kb':
        return '\b'
    return chr(int(ch))

def redraw():#刷新窗口
    vim.command("redraw")



def echoline(msg, hl = False):#在命令行, 输出一行通知信息
    hl_pre = ''
    hl_post = ''
    if hl:
        hl_pre = 'echohl   WarningMsg | '
        hl_post = ' | echohl None'
    vim.command('redraw| %s echomsg "%s" %s' %
            (hl_pre, msg.replace('"', r'\"'), hl_post) )

echo = echoline




def str_before_cursor():
    "返回光标前的字符串"
    col_nu_cursor=vim.current.window.cursor[1]
    cur_line=vim.current.line
    return cur_line[0:col_nu_cursor].decode(vim.eval('&encoding'))

def str_after_cursor():
    "返回光标后的字符串"
    col_nu_cursor=vim.current.window.cursor[1]
    cur_line=vim.current.line
    return cur_line[col_nu_cursor:].decode(vim.eval('&encoding'))

def getline( ):
    return vim.current.line

def gotofile( file_path):
    vim.command('silent update')
    vim.command("silent edit %s"  %  file_path)

def editfile(file_path):
    vim.command('silent update')
    vim.command("silent edit %s"  %  file_path)


def syntax_area( ):
    "得到当前的语法区域的名称，这个是由syntax决定的"
    command='synIDattr(synIDtrans(synID(line("."), col(".") - 1, 1)), "name")'
    return vim.eval(command)

def clear_buffer( ):
    "清空当前缓冲区"
    del vim.current.buffer[ : ]

def feedkeys(key, mode='n'):
    if isinstance(key, list):
        for s in key:
            feedkeys(s, mode)
    else:
        if key == r'"':
            key = r'\"'

        elif key == '\\':
            key = '\\\\'

        command='call feedkeys("%s", "%s")' %(key, mode)
        vim.command(command)

def pumvisible( ):
    "返回当前的pmenu是否弹出"
    return int(vim.eval( "pumvisible( )"))

def parent_search( file_name):
    "在当前文件的目录开始向上寻找file_name"
    cur_dir=os.path.dirname( vim.current.buffer.name)
    return _parent_search(cur_dir, file_name )

def _parent_search(path, file_name ):

    file_path=path + '/' + file_name
    if os.path.isfile( file_path):
        return path
    else:
        _path=os.path.dirname(path )
        if _path==path:
            return None
        else:
            return _parent_search( _path, file_name)

def is_empty( ):
    if (len(vim.current.buffer) == 1\
                and len(vim.current.buffer[0]) == 0):
        return True
    else:
        return False

def current_word( from_vim=True ):
    if from_vim:
        return vim.eval("expand('<cword>')");
    else:
        buf = []
        tmp = str_before_cursor()

        for i in range(len(tmp) -1 , -1,-1):
            c = tmp[i]

            if not (c.isalpha() or c == '_'):
                buf.append(tmp[i+1:])
                break
            if i == 0:
                buf.append(tmp)


        for c in str_after_cursor():
            if (c.isalpha() or c == '_'):
                buf.append(c)
            else:
                break

        return  ''.join(buf)

#如果有错误文件,打开quickfix
def quickfix(hight = 15):
    vim.command('botright cope %s'  % hight )


def quickfix_read_error(error_file):
    vim.command('cgetfile %s'  %  error_file)

def filepath( ):
    _path= vim.current.buffer.name
    if _path =='':
        return None
    return _path

def getchar( ):
    return chr( vim.eval('getchar()') )


def openfiles(files):
    win = vim.current.window
    if not files:
        return

    f = files[0]
    if os.path.isfile(f):
        vim.command('edit %s' % f)

    if len(files) == 1:
        return

    for f in files[1:]:
        if os.path.isfile(f):
            vim.command('vs %s' % f)

