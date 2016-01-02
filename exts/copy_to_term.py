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
    try:
        os.popen("echo '%s' | mac c" % copy)
        #requests.post('http://10.0.2.2:8080/clipboard/content',
        #        {'clipboard': copy})
        pyvim.echo('Copy TO Host')

    except:
        pyvim.echo('Copy TO Host: Fail!!!', hl=True)

@pyvim.cmd()
def PasteFromHost():
    #c = requests.get('http://10.0.2.2:8080/clipboard/content').text
    c = os.popen("mac p").read().decode('gbk').encode('utf8')
    setreg = vim.Function('setreg')
    setreg('"', c)





if __name__ == "__main__":
    pass

