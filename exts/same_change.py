# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-30 09:40:15
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import im.imrc
import pyvim
import vim

def moved():
    pyvim.log.error( vim.current.line )

handle = None

@pyvim.cmd()
def ADD():
    global  handle
    handle = pyvim.addevent('CursorMovedI', moved)

@pyvim.cmd()
def DEL():
    global  handle
    if not handle:
        return
    pyvim.delevent(handle)
    handle = None





if __name__ == "__main__":
    pass

