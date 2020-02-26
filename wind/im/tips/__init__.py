# -*- coding:utf-8 -*-
#    author    :   b'\xe4\xb8\x81\xe9\x9b\xaa\xe5\xb3\xb0'
#    time      :   2020-02-25 17:25:43
#    email     :   b'fengidri@yeah.net'
#    version   :   1.0.1



from . import path
from . import date
from . import c_include
from ..imrc import emit_event
import pyvim
import vim
import im.env as env

class g:
    last_pos = None

def do_tips():
    if pyvim.pumvisible():
        return

    pos = vim.current.window.cursor
    if pos == g.last_pos:
        return
    g.last_pos = pos

    if date.handler():
        return

    if c_include.handler():
        return

    if path.handler():
        return

def tips_handler():
    emit_event('start')

    pyvim.log.error("enter tips_handler: ft: %s", env.ft)

    do_tips()

    emit_event('pre-stop')
    emit_event('stop')
