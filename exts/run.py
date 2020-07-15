# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-05-17 11:28:33
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import pyvim
import os


@pyvim.cmd()
def Run():
    line = vim.current.line
    line = line.split('$', 1)

    if len(line) != 2:
        cmd = '!clear; make'
    else:
        cmd = line[1]

    vim.command(cmd)

