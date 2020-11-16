# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-05-17 11:28:33
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import pyvim
import os

class g:
    last = None

@pyvim.cmd()
def Run(cmd = None):
    if not cmd:
        if not g.last:
            return

        cmd = g.last
    else:
        g.last = cmd

    root = pyvim.get_cur_root()
    if root:
        cmd = '!cd %s;%s' % (root, cmd)
    else:
        cmd = '!%s' % (cmd,)

    vim.command(cmd)


@pyvim.cmd()
def R(cmd = None):
    Run(cmd)
