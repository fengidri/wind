# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-01-26 13:45:16
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import vim
import logging

log = logging.getLogger("wind")

__Event_Map = {}
__Event_Index = 0

def event_callback( cbid ):#事件回调函数  @event: 当前的事件
    log.debug("callback event: %s" % cbid)
    cb = __Event_Map.get(cbid)
    if not cb:
        logging.error("Not Found cb for: %s" % cbid)
        return

    cb[0](*cb[1])



def addevent(event, cb, pat='*', arg  = ()):
    global __Event_Index
    __Event_Index += 1

    autocmd_cmd_format = "autocmd {event} {pat} {cmd}"

    cbid = "%s_%s" % (cb.__code__.co_name, __Event_Index)
    log.error("addevent: %s" % cbid)
    cmd = "py3 IM('event', '%s')" % cbid
    __Event_Map[cbid] = (cb, arg)

    if not isinstance(pat, str):
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

