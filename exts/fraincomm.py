# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import pyvim
import vim
import os
@pyvim.cmd()
def ProjectTerminal():
    name = vim.current.buffer.name
    for p in pyvim.Roots:
        if name.startswith(p):
            os.system('cd %s;setsid xterm&' % p)
            break

    else:
        os.system('setsid xterm&')




