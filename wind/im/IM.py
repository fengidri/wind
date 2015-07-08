#encoding:utf8
import os
import sys
from pyvim import log
import pyvim

import stream
import prompt
import setting
from imrc import emit_event

def IM_Init():
    stream.Init()
    prompt.Init()

def IM(*args):
    """
       处理事件.
       @tp: 表示当前的收到的事件的类型
       @event: 收到的事件

       tp 可以是 digit, upper, lower, punc, mult 也可以是 event
    """

    log.error('-----------------------------------------------')

    cls = args[0]
    emit_event('start')

    if cls == "prompt":
        prompt.handle(*args[1:])

    elif cls == "key":
        stream.handle(*args[1:])

    elif cls == "setting":
        setting.handle(*args[1:])

    elif cls == "command":
        pyvim.cmd_cb(*args[1:])

    elif cls == "event":
        pyvim.event_callback(*args[1:])




    emit_event('pre-stop')

    emit_event('stop')


if __name__ != "__main__":
    IM_Init()
