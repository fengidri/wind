# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-06 10:12:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import vim
from .imrc  import hook
import pyvim

before   = ''
after    = ''
vchar    = ''
encoding = ''
col      = 0
num      = 0
ft       = ''
syntax   = ''
pumvisible = False

@hook('start')
def init():
    global before
    global after
    global encoding
    global vchar
    global col
    global num
    global ft
    global syntax
    global pumvisible

    pumvisible = pyvim.pumvisible()

    ft       = vim.eval('&ft')
    encoding = vim.eval('&encoding')
    vchar    = vim.eval('v:char')

    num, col = vim.current.window.cursor

    line = vim.current.line

    line = bytes(line,  encoding="utf-8")

    before = line[0: col].decode('utf8')
    after = line[col:].decode('utf8')

    command='synIDattr(synIDtrans(synID(line("."), col(".") - 1, 1)), "name")'
    syntax = vim.eval(command)
    if not after: # some time the last char in the line may not active
        syntax = vim.eval(command)




if __name__ == "__main__":
    pass

