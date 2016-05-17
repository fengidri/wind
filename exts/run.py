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
    cmd = None
    for line in vim.current.buffer:
        c = line.find('$')
        if c > -1:
            cmd = line[c + 1:]
            break
    if not cmd:
        pyvim.echo('Not Found Cmd')
    else:
        os.popen2(cmd)
        pyvim.echo('Run: %s' % (cmd,))

