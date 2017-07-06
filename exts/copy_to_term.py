# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-09-16 07:10:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import pyvim
import sys
import os
import requests

COPY_BOARD_FILE = "/dev/shm/vim_copy_board"


@pyvim.cmd()
def CopyToIterm2():
    cmd = "\033]50;CopyToClipboard=\a%s\033]50;EndCopy\a"
    sel = vim.eval('@0')
    cmd = cmd % sel

    os.system('echo -e "%s" '%(cmd))

    vim.command("redraw!")


@pyvim.cmd()
def CopyToHost():
    getreg = vim.Function("getreg")
    copy = getreg('"')

    open(COPY_BOARD_FILE, 'w').write(copy)

@pyvim.cmd()
def PasteFromHost():

    c = ""
    if os.path.isfile(COPY_BOARD_FILE):
        c = open(COPY_BOARD_FILE).read()


    setreg = vim.Function('setreg')
    setreg('"', c)





if __name__ == "__main__":
    pass

