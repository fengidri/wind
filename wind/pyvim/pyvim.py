# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import os
import logging
import logging.handlers
import sys
LOGFILE = "/tmp/vimlog"
MAXBYTES = 1024 * 1024 * 10

logging.basicConfig(filename=LOGFILE + '1', level=logging.DEBUG)

handlers = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=MAXBYTES)
#formatter = ">>%(message)s"
#handlers.setFormatter(formatter)

log = logging.getLogger("Wind")
log.setLevel(logging.DEBUG)
log.addHandler(handlers)

log.error("\n\n\n\n\n\nVIM Start.............................")

def excepthook(type, value, trace):
    if type == KeyboardInterrupt:
        print ""
        return
    echoline(">>Error(%s): %s: " % (LOGFILE, type.__name__ + str(value)))

    log.error("Uncaught exception:", exc_info =(type, value, trace))

sys.excepthook = excepthook

def origin_win( ):
    vim.command( "wincmd p")

def win_max( ):
    vim.command( "set lines=999" )
    vim.command( "set columns=999")


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

class SelMenu( object ):
    "基于omnicomplete 包装成的SelMenu"
    "默认使用内部的complete function"
    "也可以指定omnicomplete function "

    omnifunc = "vimlib#SelMenuFunction"
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(SelMenu, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def check_omnifunc( self, func ):
        if vim.eval( '&l:omnifunc' ) != func:
            vim.command("let &omnifunc='%s'" % func)
            vim.command("let &l:omnifunc='%s'" % func)

    def showlist(self, words_list, length):
        """ 与show 比较相似, 只是使用 输入的是list, 也就说是比较简单的结构"""
        words = []
        for w in words_list:
            words.append({"word": w})
        self.show(words, length)

    def show( self, words, length ):
        """使用内部的补全函数进行输出
                @words:   vim 格式的数据结构
                @length:  光标前要进行补全的字符长度
        """
        self.words = words
        vim.vars["omniresult"] = words
        vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1
        self.complete(self.omnifunc)


    def complete(self, fun):
        "指定补全函数"
        self.check_omnifunc(fun)
        feedkeys('\<C-X>\<C-O>\<C-P>',  'n')

    def select(self, nu):
        if pumvisible( ):
            feedkeys((nu + 1) * '\<C-N>' , 'n' )
            feedkeys( '\<C-Y>', 'n' )

    def getselect(self, nu):
        if pumvisible( ):
            feedkeys( '\<C-Y>', 'n' )
        return self.words[nu]

    def cencel( self ):
        feedkeys('\<C-e>', 'n')




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
        buf = [   ]
        tmp = str_before_cursor( )

        for i in range(len(tmp) -1 , -1,-1):
            c = tmp[ i ]

            if not (c.isalpha( ) or c == '_'):
                buf.append( tmp[i+1:] )
                break
            if i == 0:
                buf.append( tmp)


        for c in str_after_cursor( ):
            if (c.isalpha( ) or c == '_'):
                buf.append( c )
            else:
                break

        return  ''.join( buf )

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

