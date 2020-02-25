# -*- coding:utf-8 -*-
#    author    :   b'\xe4\xb8\x81\xe9\x9b\xaa\xe5\xb3\xb0'
#    time      :   2020-02-25 15:06:18
#    email     :   b'fengidri@yeah.net'
#    version   :   1.0.1


import vim
from .pyvim import log

timer_ids = {}

def timerstart(ms, callback):

    cmd = 'timer_start(%s, "wind#TimerHandler")' % ms

    timerid = vim.eval(cmd)

    log.error("timerstart: %s", timerid)

    timer_ids[timerid] = (callback, )

    return timerid

def timerstop(timerid):
    vim.eval('timer_stop(%s)' % timerid)
    del timer_ids[timerid]


def timercall(timerid):

    log.error("timercall: %s", timerid)

    cb = timer_ids.get(timerid)
    if not cb:
        return

    cb[0]()


