# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:40:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from events import EventNames
import os
import vim
import logging

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

