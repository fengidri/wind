#encoding:utf8
import os
import sys
from pyvim import log

import stream
import prompt
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

    #elif cls == "event":
    #    redirect(*args)

    emit_event('pre-stop')

    emit_event('stop')
    #elif pyvim.pumvisible():
    #    if not call('prompt', event, tp):
    #        redirect(event, tp)

if __name__ != "__main__":
    IM_Init()
