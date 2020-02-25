#encoding:utf8
import os
import sys
from pyvim import log
import pyvim
import vim

from . import stream
from . import prompt
from . import setting
import frainui
from .imrc import emit_event


RouteMap = {
        "prompt":       prompt.handle,
        "key":          stream.handle,
        "setting":      setting.handle,
        "command":      pyvim.cmd_cb,
        "event":        pyvim.event_callback,
        "cmd_complete": pyvim.command_complete,
        "frainui":      frainui.handle,
        }

def IM(*args):
    """
       处理事件.
       @tp: 表示当前的收到的事件的类型
       @event: 收到的事件

       tp 可以是 digit, upper, lower, punc, mult 也可以是 event
    """
    log.debug('IM >>>> %s <<<<', args)

    emit_event('start')

    cls = args[0]
    handle = RouteMap.get(cls)
    if handle:
        handle(*args[1:])
    else:
        log.error("IM: Not Found Cls: %s", cls)

    emit_event('pre-stop')

    emit_event('stop')

