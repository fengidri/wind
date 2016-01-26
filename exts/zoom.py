# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-01-02 13:40:49
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log
from pyvim import cmd
import vim
import logging
import pyvim


class Z:
    bnr = None
    title = ''


@cmd()
def Zoom():
    if Z.bnr == None:
        vim.vars['wind_zoom'] = 'Z'
        Z.bnr = vim.current.buffer.number
        vim.command("tab split")

        Z.title = pyvim.Title
        pyvim.settitle('%s*Z' % Z.title)

    else:
        pyvim.settitle(Z.title)

        vim.vars['wind_zoom'] = 'z'
        cursor = vim.current.window.cursor
        bnr = vim.current.buffer.number
        vim.command("tabclose")
        if bnr == vim.current.buffer.number:
            vim.current.window.cursor = cursor
            Z.bnr = None



if __name__ == "__main__":
    pass


