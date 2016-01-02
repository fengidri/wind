# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-01-02 13:40:49
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log
from pyvim import cmd
import vim
import logging

restcmd = None
win_to_buffer = {}

winrestcmd = vim.Function('winrestcmd')

@cmd()
def Zoom():
    global restcmd
    global win_to_buffer
    if not restcmd:
        cur = vim.current.window
        for w in vim.windows:
            win_to_buffer[w.number] = w.buffer.number
        restcmd = winrestcmd()
        vim.command('only')
    else:
        cur = vim.current.window
        vim.command('only')
        l = len(win_to_buffer)
        for i in range(l - 1):
            vim.command('vs')

        vim.command("%s" % restcmd)
        for w, b in win_to_buffer.items():
            vim.command("%swindo b %s" % (w, b))

        vim.current.window = cur
        restcmd = None
        win_to_buffer = {}



if __name__ == "__main__":
    pass


