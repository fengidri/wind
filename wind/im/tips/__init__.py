# -*- coding:utf-8 -*-
#    author    :   b'\xe4\xb8\x81\xe9\x9b\xaa\xe5\xb3\xb0'
#    time      :   2020-02-25 17:25:43
#    email     :   b'fengidri@yeah.net'
#    version   :   1.0.1



from . import path
from . import date
from ..imrc import emit_event
import pyvim
import vim

class g:
    last_pos = None

def do_tips():
    pos = vim.current.window.cursor
    if pos == g.last_pos:
        return
    g.last_pos = pos

    if pyvim.pumvisible():
        return

    if date.handler():
        return

    if path.handler():
        return

def tips_handler():
    emit_event('start')

    do_tips()

    emit_event('pre-stop')
    emit_event('stop')
