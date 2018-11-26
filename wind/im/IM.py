#encoding:utf8
import os
import sys
from pyvim import log
import pyvim
import vim

import stream
import prompt
import timer
import setting
import frainui
from imrc import emit_event


RouteMap = {
        "prompt":       prompt.handle,
        "timer":        timer.handle,
        "key":          stream.handle,
        "setting":      setting.handle,
        "command":      pyvim.cmd_cb,
        "event":        pyvim.event_callback,
        "cmd_complete": pyvim.command_complete,
        "frainui":      frainui.handle,
        }



def IM_Init():
    stream.Init()


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


if __name__ == "__main__":
    IM_Init()
