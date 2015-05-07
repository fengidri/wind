# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:40:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from events import EventNames
import os
import vim
import logging
class complete(object):
    augroup       = "augroup"               # autocmd groups
    buffer        = "buffer"                # buffer names
    behave        = "behave"                # :behave suboptions
    color         = "color"                 # color schemes
    command       = "command"               # Ex command (and arguments)
    compiler      = "compiler"              # compilers
    cscope        = "cscope"                # |:cscope| suboptions
    dir           = "dir"                   # directory names
    environment   = "environment"           # environment variable names
    event         = "event"                 # autocommand events
    expression    = "expression"            # Vim expression
    file          = "file"                  # file and directory names
    file_in_path  = "file_in_path"          # file and directory names in |'path'|
    filetype      = "filetype"              # filetype names |'filetype'|
    function      = "function"              # function name
    help          = "help"                  # help subjects
    highlight     = "highlight"             # highlight groups
    history       = "history"               # :history suboptions
    locale        = "locale"                # locale names (as output of locale -a)
    mapping       = "mapping"               # mapping name
    menu          = "menu"                  # menus
    option        = "option"                # options
    shellcmd      = "shellcmd"              # Shell command
    sign          = "sign"                  # |:sign| suboptions
    syntax        = "syntax"                # syntax file names |'syntax'|
    syntime       = "syntime"               # |:syntime| suboptions
    tag           = "tag"                   # tags
    tag_listfiles = "tag_listfiles"         # tags, file names are shown when CTRL-D is hit
    user          = "user"                  # user names
    var           = "var"                   # user variables

###################################
# Command Api
###################################
def funnargs(fun):
    nargs = len(fun.func_code.co_varnames)
    pargs = fun.func_code.co_argcount # pos args
    dargs = 0
    if fun.func_defaults:
        dargs = len(fun.func_defaults)    # default args
    _min = pargs - dargs
    if nargs > pargs:
        _max = 10000000
    else:
        _max = nargs
    return (_min, _max)


CMDS = []
def __command(vimcmd, fun, complete):
    vimcmd = vimcmd[0].upper() + vimcmd[1:]

    _min, _max = funnargs(fun)
    if _min == _max:
        if _min == 0:
            nargs = '-nargs=0'
        elif _min == 1:
            nargs = '-nargs=1'
        else:
            nargs = '-nargs=+'
    elif _max == 0:
        nargs = '-nargs=0'
    elif _min == 0:
        if _max == 1:
            nargs = '-nargs=?'
        else:
            nargs = '-nargs=*'
    else:
        nargs = '-nargs=+'

    command = "command {args} {complete} {vimcmd} " \
                    "py {module}.cmd_cb({index}, '<args>')"

    c = command.format(args = nargs, complete= complete, vimcmd = vimcmd,
            module=__name__, index=len(CMDS))
    CMDS.append(fun)
    logging.error(c)
    vim.command(c)


def cmd_cb(index, args):
    fun  = CMDS[index]
    args =  args.split()

    _min, _max = funnargs(fun)
    if len(args) >= _min and len(args) <= _max:
        fun(*args)
    else:
        logging.error("fun:%s args should [%s, %s]. Now %s", _min, _max,
                ' '.join(args))




def cmd(complete = None):
    if isinstance(complete, list):
        complete = "-complete=%s" % ','.join(complete)

    elif isinstance(complete, basestring):
        complete = "-complete=%s" % complete

    else:
        complete = ""

    def _cmd(fun):
        __command(fun.func_code.co_name, fun, complete)

    return _cmd




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

    def __init__( self, index ):
        self.complete_type = ""
        self.setting( )

        if self.complete_type != '':
            self.complete_type = "-complete=%s" % self.complete_type
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
            if not event in EventNames:
                continue

            callback = getattr( self, attr)
            addevent(event, self.pats.get(callback , '*'), callback)

    def set_pat(self, callback, pat):#为某个事件设置, 触发的文件条件
        self.pats[callback] = pat

    def setting(self):
        pass


def event_callback( event ):#事件回调函数  @event: 当前的事件
    callback_list = events.event_callback.get( event )
    if  callback_list:
        for callback in callback_list:
            callback( )

def addevent(e, pat, cb):
    event = '%s %s' % (e, pat)
    cblist = events.event_callback.get(event)
    if not cblist:
        cmd = "au  %s py %s.event_callback('%s') " % \
                ( event, __name__, event )
        vim.command( cmd )
        events.event_callback[ event ] = [ cb ]
    else:
        cblist.append(cb)





def load_plugin( pyplugin_path ):
    modes = os.listdir( pyplugin_path )
    for mode in modes:
        if not mode.endswith( ".py" ):
            continue
        mode = mode.split( '.' )[ 0 ]
        try:
            mode = __import__( mode )
        except Exception, why:
            import traceback
            logging.error(traceback.format_exc())
            print "pyplugin: Load Error:\n%s: %s" %( mode, why)








if __name__ == "__main__":
    pass

