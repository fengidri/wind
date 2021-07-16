# -*- coding:utf-8 -*-

import popup
import pyvim
import vim

class g:
    history = []


def callback(cmd):
    if not cmd:
        return

    vim.command(cmd)


def history(key, cmd = ''):
    i = popup.PopupMenuItem(key, callback, cmd)
    g.history.insert(0, i)


@pyvim.cmd()
def History():

    popup.PopupMenu(g.history, hotkey = False, title = 'History')








