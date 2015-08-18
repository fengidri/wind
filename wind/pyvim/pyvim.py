# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import os
import logging
log = logging.getLogger("wind")

import plugin


# for previous
__previous = None
def previous():
    return __previous

@plugin.event("WinLeave")
def _previous():
    global __previous
    __previous = vim.current.window


# 记录窗口跳转的过程
class WStack(dict):
    def __init__(self):
        pass


    def append(self):
        bn = vim.current.buffer.number
        cursor = vim.current.window.cursor

        pos = (bn, cursor)

        stack = self.get(vim.current.window)
        if not stack:
            self[vim.current.window] = [pos]
        else:
            stack.append(pos)

    def pop(self, pos):
        stack = self.get(vim.current.window)
        if not stack:
            return
        else:
            return stack.pop()


def settitle(name):#设置vim 窗口的title
    # 如果没有设置name, 则使用第一个root的name
    vim_title = name.replace( ' ', '\\ ')
    vim.command( "set title titlestring=%s" % vim_title )


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



class _get_input:
    def __init__(self):
        self.str_before_cursor=''
        self.str_after_cursor=''
        self.line_nu_cursor=0
        self.col_nu_cursor=0
        self.len_before_cursor=0

    def update(self):
        self.line_nu_cursor, self.col_nu_cursor=vim.current.window.cursor
        cur_line=vim.current.line
        self.str_before_cursor= cur_line[0:self.col_nu_cursor]
        self.str_after_cursor=cur_line[self.col_nu_cursor:]
        self.len_before_cursor=len(self.str_before_cursor)


    def key(self):
        str_after_cursor=self.str_after_cursor
        str_before_cursor=self.str_before_cursor
        line_nu_cursor=self.line_nu_cursor
        col_nu_cursor=self.col_nu_cursor
        len_before_cursor=self.len_before_cursor
        update(self)

        if line_nu_cursor != self.line_nu_cursor:
            'move up or down'
            return None

        elif str_after_cursor != self.str_after_cursor:
            'move left or right'
            return None

        elif len_before_cursor > self.len_before_cursor:
            return '<backspace>'

        else:
            str_tmp=self.str_before_cursor[len_before_cursor:]
            return self.key_check(str_tmp)

    def key_check(self):
        if len(str_tmp) == 1:
            return str_tmp
        else:
            return None

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
    vim.command('edit %s' % files[0])
    for f in files[1:]:
        vim.command('vs %s' % files[0])


if __name__ == "__main__":
    pass

