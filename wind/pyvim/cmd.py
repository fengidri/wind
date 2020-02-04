# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:40:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import vim
import logging

log = logging.getLogger("wind")

CMDS = []
CMD_OPTS = {}


###################################
# Command Api
###################################
def funnargs(fun):
    nargs = len(fun.__code__.co_varnames)
    pargs = fun.__code__.co_argcount # pos args
    dargs = 0
    if fun.__defaults__:
        dargs = len(fun.__defaults__)    # default args
    _min = pargs - dargs
    if nargs > pargs:
        _max = 10000000
    else:
        _max = nargs
    return (_min, _max)

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
                    "py3 IM('command', {index}, '<args>')"

    c = command.format(args = nargs, complete= complete, vimcmd = vimcmd,
            index=len(CMDS))

    CMDS.append(fun)
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
    if isinstance(complete, list) or isinstance(complete, dict):
        opts = complete
        complete = "-complete=customlist,wind#CommandsComplete"

    elif isinstance(complete, str):
        complete = "-complete=%s" % complete

    else:
        complete = ""

    def _cmd(fun):
        name = fun.__code__.co_name
        CMD_OPTS[name] = opts
        __command(name, fun, complete)
        return fun

    return _cmd

def command_complete(arglead, cmdline, cursorpos):
    t = cmdline.split()
    if arglead:
        del t[-1]

    cmd = t[0]
    if len(t) > 1:
        args = cmdline.split()[1:]
    else:
        args = []

    opts = CMD_OPTS.get(cmd, [])
    for a in args:
        if not isinstance(opts, dict):
            return
        opts = opts.get(a, [])

    if isinstance(opts, dict):
        opts = opts.keys()

    opts = [o for o in opts if o.startswith(arglead)]
    vim.vars['wind_commands_complete'] = opts

