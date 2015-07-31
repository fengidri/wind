# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:40:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from events import EventNames
import os
import vim
from pyvim import log as logging

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
CMD_OPTS = {}

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
                    "py IM('command', {index}, '<args>')"

    c = command.format(args = nargs, complete= complete, vimcmd = vimcmd,
            index=len(CMDS))

    CMDS.append(fun)
    logging.debug(c)
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
    """
    Decorator: Add new command.
    @param complete:
            complete 参数用于指定命令的补全特性. 如果complete 是一个list
            list 的item 做为命令的子命令
    """
    opts = []
    if isinstance(complete, list):
        opts = complete
        complete = "-complete=customlist,wind#CommandsComplete"

    elif isinstance(complete, basestring):
        complete = "-complete=%s" % complete

    else:
        complete = ""

    def _cmd(fun):
        name = fun.func_code.co_name
        CMD_OPTS[name] = opts
        __command(name, fun, complete)
        return fun

    return _cmd

def command_complete(arglead, cmdline, cursorpos):
    cmd = cmdline.split()[0]
    opts = [ o for o in CMD_OPTS.get(cmd, []) if o.startswith(arglead)]

    vim.vars['wind_commands_complete'] = opts





__Event_Map = {}
__Event_Index = 0

def event_callback( cbid ):#事件回调函数  @event: 当前的事件
    cb = __Event_Map.get(cbid)
    if not cb:
        logging.error("Not Found cb for: %s" % cbid)
        return
    cb()



def addevent(event, cb, pat='*'):
    global __Event_Index
    __Event_Index += 1

    autocmd_cmd_format = "autocmd {event} {pat} {cmd}"

    cbid = "%s_%s" % (cb.func_code.co_name, __Event_Index)
    cmd = "py IM('event', '%s')" % cbid
    __Event_Map[cbid] = cb

    if not isinstance(pat, basestring):
        pat = "<buffer=%s>" % pat.number

    autocmd_cmd =  autocmd_cmd_format.format(event = event, pat = pat, cmd = cmd)
    vim.command("augroup %s" % cbid)
    vim.command(autocmd_cmd)
    vim.command("augroup END")

    return (cbid, event, pat, cmd)

def delevent(evhandle):
    vim.command("autocmd! %s" % evhandle[0])
    del __Event_Map[evhandle[0]]




def event(e, pat='*'):
    def _f(func):
        addevent(e, func, pat)
        return func
    return _f


if __name__ == "__main__":
    pass

