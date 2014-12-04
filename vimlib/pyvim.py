#encoding:utf8
#对于vim的一些操作的封装
import os
import sys
import re
import logging
import vim

vim_events=[ 
        "BufNewFile"		,
        "BufReadPre"		,
        "BufRead"		,
        "BufReadPost"		,
        "BufReadCmd"		,
        "FileReadPre"		,
        "FileReadPost"		,
        "FileReadCmd"		,
        "FilterReadPre"		,
        "FilterReadPost"	,
        "StdinReadPre"		,
        "StdinReadPost"		,
        "BufWrite"		,
        "BufWritePre"		,
        "BufWritePost"		,
        "BufWriteCmd"		,
        "FileWritePre"		,
        "FileWritePost"		,
        "FileWriteCmd"		,
        "FileAppendPre"		,
        "FileAppendPost"	,
        "FileAppendCmd"		,
        "FilterWritePre"	,
        "FilterWritePost"	,
        "BufAdd"		,
        "BufCreate"		,
        "BufDelete"		,
        "BufWipeout"		,
        "BufFilePre"		,
        "BufFilePost"		,
        "BufEnter"		,
        "BufLeave"		,
        "BufWinEnter"		,
        "BufWinLeave"		,
        "BufUnload"		,
        "BufHidden"		,
        "BufNew"		,
        "SwapExists"		,
        "FileType"		,
        "Syntax"		,
        "EncodingChanged"	,
        "TermChanged"		,
        "VimEnter"		,
        "GUIEnter"		,
        "GUIFailed"		,
        "TermResponse"		,
        "QuitPre"		,
        "VimLeavePre"		,
        "VimLeave"		,
        "FileChangedShell"	,
        "FileChangedShellPost"	,
        "FileChangedRO"		,
        "ShellCmdPost"		,
        "ShellFilterPost"	,
        "FuncUndefined"		,
        "SpellFileMissing"	,
        "SourcePre"		,
        "SourceCmd"		,
        "VimResized"		,
        "FocusGained"		,
        "FocusLost"		,
        "CursorHold"		,
        "CursorHoldI"		,
        "CursorMoved"		,
        "CursorMovedI"		,
        "WinEnter"		,
        "WinLeave"		,
        "TabEnter"		,
        "TabLeave"		,
        "CmdwinEnter"		,
        "CmdwinLeave"		,
        "InsertEnter"		,
        "InsertChange"		,
        "InsertLeave"		,
        "InsertCharPre"		,
        "ColorScheme"		,
        "RemoteReply"		,
        "QuickFixCmdPre"	,
        "QuickFixCmdPost"	,
        "SessionLoadPost"	,
        "MenuPopup"		,
        "CompleteDone"		,
        "User"			,
        ]
#}}}

def origin_win( ):
    vim.command( "wincmd p")
def win_max( ):
    vim.command( "set lines=999" )
    vim.command( "set columns=999")
class _log:
    def __init__(self):
        self.level= 3

    def fatal(self,msg):
        return

    def error(self,msg):
        return

    def warning(self,msg):
        return

    def info(self,msg):
        return

    def debug(self,msg):
        return

    def write(self,msg):
        return 


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

class stdin( object ):
    def read(self, message = ''):
        vim.command('call inputsave()')
        vim.command("let user_input = input('" + message + "')")
        vim.command('call inputrestore()')
        print( "" )
        return vim.eval('user_input')

class stdout( object ):
    def write( self, message ):
        print message


def getchr():#getchr
    ch=vim.eval("getchar()")
    if ch == '\x80kb':
        return '\b'
    return chr(int(ch))

def redraw():#刷新窗口
    vim.command("redraw")

def echoline(msg):
    vim.command('redraw| echo "%s"' % msg.replace('"', r'\"') )




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
class _pmenu( object ):
    def __init__(self):
        self.omnifunc = ""
        self.omnifunc_save = ""


    def check_omnifunc( self, func ):
        if vim.eval( '&l:omnifunc' ) != func:
            vim.command("let &omnifunc='%s'" % func)
            vim.command("let &l:omnifunc='%s'" % func)


    def show( self, func="" ):
        logging.info("Pmenu show")
        
        self.check_omnifunc(func)
        feedkeys('\<C-X>\<C-O>\<C-P>',  'n')


    def select( self, nu):
        if pumvisible( ):
            feedkeys((nu + 1) * '\<C-N>' , 'n' )
            feedkeys( '\<C-Y>', 'n' )

    def cencel( self ):
        feedkeys('\<C-e>', 'n')
   



def str_before_cursor():
    "返回光标前的字符串"
    col_nu_cursor=vim.current.window.cursor[1]
    cur_line=vim.current.line
    return cur_line[0:col_nu_cursor]

def str_after_cursor():
    "返回光标后的字符串"
    col_nu_cursor=vim.current.window.cursor[1]
    cur_line=vim.current.line
    return cur_line[col_nu_cursor:]
def getline( ):
    return vim.current.line

def gotofile( file_path):
    vim.command('silent update')
    vim.command("silent edit %s"  %  file_path)


def syntax_area( ):
    "得到当前的语法区域的名称，这个是由syntax决定的"
    command='synIDattr(synIDtrans(synID(line("."), col(".")-1, 1)), "name")'
    return vim.eval( command)

def clear_buffer( ):
    "清空当前缓冲区"
    del vim.current.buffer[ : ]

def feedkeys(string, mode='m'):
    string = string.replace(r'"',r'\"')
    command='call feedkeys("%s", "%s")' %(string, mode)
    
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



def highlight():
    pass
        #高亮 MarkJust
#        vim.command('MarkJust')


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

###################################
# Command Api
###################################
"""
    使用metaclass, 拦截了类对象的创建过程, 并在这个过程中自动创建实例.
    使用这个方式取代了之前的实例化方法(通过扫描模块空间中的所有的对象, 
    找到command 与events 的子类, 并实例化)
"""

class CommandMetaClass(type):
    objs = [  ]
    def __new__(cls, name, bases, dct):
        cls_command = type.__new__(cls, name, bases, dct)
        if name != "command":
            cls.objs.append( cls_command(len(cls.objs))  )
        return cls_command

def command_callback(index, argv):
    CommandMetaClass.objs[ index ].pre_run( argv )

class command( object ):
    __metaclass__ = CommandMetaClass
    complete_augroup       = "-complete=augroup"               # autocmd groups
    complete_buffer        = "-complete=buffer"                # buffer names
    complete_behave        = "-complete=behave"                # :behave suboptions
    complete_color         = "-complete=color"                 # color schemes
    complete_command       = "-complete=command"               # Ex command (and arguments)
    complete_compiler      = "-complete=compiler"              # compilers
    complete_cscope        = "-complete=cscope"                # |:cscope| suboptions
    complete_dir           = "-complete=dir"                   # directory names
    complete_environment   = "-complete=environment"           # environment variable names
    complete_event         = "-complete=event"                 # autocommand events
    complete_expression    = "-complete=expression"            # Vim expression
    complete_file          = "-complete=file"                  # file and directory names
    complete_file_in_path  = "-complete=file_in_path"          # file and directory names in |'path'|
    complete_filetype      = "-complete=filetype"              # filetype names |'filetype'|
    complete_function      = "-complete=function"              # function name
    complete_help          = "-complete=help"                  # help subjects
    complete_highlight     = "-complete=highlight"             # highlight groups
    complete_history       = "-complete=history"               # :history suboptions
    complete_locale        = "-complete=locale"                # locale names (as output of locale -a)
    complete_mapping       = "-complete=mapping"               # mapping name
    complete_menu          = "-complete=menu"                  # menus
    complete_option        = "-complete=option"                # options
    complete_shellcmd      = "-complete=shellcmd"              # Shell command
    complete_sign          = "-complete=sign"                  # |:sign| suboptions
    complete_syntax        = "-complete=syntax"                # syntax file names |'syntax'|
    complete_syntime       = "-complete=syntime"               # |:syntime| suboptions
    complete_tag           = "-complete=tag"                   # tags
    complete_tag_listfiles = "-complete=tag_listfiles"         # tags, file names are shown when CTRL-D is hit
    complete_user          = "-complete=user"                  # user names
    complete_var           = "-complete=var"                   # user variables

    def __init__( self, index ):
        self.complete_type = ""
        self.setting( )
        self.params = [  ]

        cmd_name = self.__class__.__name__
        py_name = "py %s.command_callback(%s, '<args>')" %(__name__, index)
        cmd = "command -nargs=? %s  %s %s" %\
                ( self.complete_type,cmd_name, py_name)
        vim.command( cmd )
    def pre_run( self, args ):
        self.params = args.split( )
        self.run( )
    def run( self ):
        pass
    def setting( self ):
        pass
    def set_complete( self, key ):
        self.complete_type = key
###################################
# event Api
###################################
class EventMetaClass(type):
    objs = [  ]
    def __new__(cls, name, bases, dct):
        cls_event = type.__new__(cls, name, bases, dct)
        if name != "events":
            cls.objs.append( cls_event()  )
        return cls_event


class events( object ):
    __metaclass__ = EventMetaClass

    event_callback = {}
    def __init__( self ):
        self.load_now = True
        self.pats = {}
        self.setting( )
        for attr in dir(self):
            if not (attr.startswith( "on_" ) and len(attr) > 3):
                continue

            event = attr[ 3: ]
            if not event in vim_events:
                continue

            callback = getattr( self, attr)
            event = "%s %s" % (event ,self.pats.get(callback , '*')) 
            self.add_event( event, callback )

    def get_callback_list( self, event ):
        callback_list=  self.event_callback.get( event )
        if  callback_list:
            return callback_list
        else:
            cmd = "au  %s py %s.event_callback('%s') " % \
                    ( event, __name__, event )
            vim.command( cmd )
            self.event_callback[ event ] = [  ]
            return self.event_callback[ event ]

    def add_event( self, event,  call):
        callback_list = self.get_callback_list( event )
        callback_list.append( call )

    def set_pat(self, callback, pat):#为某个事件设置, 触发的文件条件
        self.pats[callback] = pat

    def setting(self):
        pass


def event_callback( event ):#事件回调函数  @event: 当前的事件
    callback_list = events.event_callback.get( event )
    if  callback_list:
        for callback in callback_list:
            callback( )

        
def load_plugin( pyplugin_path ):
    modes = os.listdir( pyplugin_path )
    for mode in modes:
        if not mode.endswith( ".py" ):
            continue
        mode = mode.split( '.' )[ 0 ]
        try:
            mode = __import__( mode )
        except Exception, why :
            print "pyplugin:  Load plugin Error:\n%s: %s" %( mode, why)



if not __name__== "__main__":
    get_input=_get_input()
    pmenu = _pmenu()
    log=_log()





