# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 10:12:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import vim
import imutils

before = ''
after = ''
vchar = ''
encoding = ''
col = 0
num = 0

@imutils.hook('start')
def init():
    global before
    global after
    global encoding
    global vchar
    global col
    global num


    encoding = vim.eval('&encoding')
    vchar = vim.eval('v:char')

    num, col = vim.current.window.cursor
    line = vim.current.line

    before = line[0: col].decode(encoding)
    after = line[col:].decode(encoding)

if __name__ == "__main__":
    pass

