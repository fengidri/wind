# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-29 17:15:16
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import vim
from pyvim  import log as logging

@pyvim.cmd()
def Poshl():
        start = vim.eval('getpos("\'<")')
        end   = vim.eval('getpos("\'>")')

        start = (int(start[1]), int(start[2]))
        end   = (int(end[1]),   int(end[2]) + 1)
        poshl(start, end)

def poshl(s, e):
    st = "\\%%%dl\\%%%dc" % s
    en = "\\%%%dl\\%%%dc" % e
    cmd = 'syntax region Todo start=/%s/ end=/%s/' % (st, en)
    logging.info(cmd)

    vim.command(cmd)

if __name__ == "__main__":
    pass

