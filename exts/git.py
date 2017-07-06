# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-06-16 10:00:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import pyvim
import os


@pyvim.cmd()
def GS():
    gs = os.popen('git status')


@pyvim.cmd()
def GitBlame():
    #TODO clear all window scrollbind


    prewin = vim.current.window

    f = vim.current.buffer.name
    lines = os.popen("git blame %s" %f).readlines()
    for i, line in enumerate(lines):
        lines[i] = line.split(')')[0] + ')'

    vim.command("setlocal scrollbind")

    vim.command("50vnew")

    vim.current.buffer[0:] = lines

    vim.command("setlocal nomodifiable")
    vim.command("setlocal noswapfile")
    vim.command("setlocal scrollbind")
    vim.command("setlocal buftype=nofile")

    vim.current.window = prewin
