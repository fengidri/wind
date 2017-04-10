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
        pyvim.echo('Not Found Cmd')
        return

    cmd = line[1]

    f = os.popen(cmd)
    pyvim.echo('Run: %s' % (cmd,))

    #for line in f.readlines():
    #    pyvim.echo(line.strip())

