# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-10-09 19:40:27
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim
from frainui import tmpedit

@pyvim.cmd()
def CFunComment():
        Comment().fun_comment()

class Comment(object):
    def __init__(self):
        self.funline = 0 # 函数所在行
        self.statement = ""
        self.args = None
        self.funname = ""




    def get_statement(self):
        curline = vim.current.window.cursor[0] # 当前光标行
        start = end = False
        lines = []
        offset = -1
        for line in vim.current.buffer[curline:]:
            offset += 1
            if line.find('(') > -1:
                start = True
                self.funline = curline + offset
            if line.find(')') > -1:
                end = True
            if start:
                lines.append(line)
            if end:
                break
        self.statement =  ' '.join(lines)

    def get_args(self):

        start = self.statement.find('(')
        end   = self.statement.find(')')
        if start < 0 or end < 0:
            return

        argslist = self.statement[start + 1: end]
        argparts = argslist.split(',')
        args = []
        for argpart in argparts:
            arg = argpart.split()[-1]
            if arg.startswith('*'):
                arg = arg.split('*')[-1]
            args.append(arg)
        self.args = args

    def get_funname(self):
        start = self.statement.find('(')
        if start < 0:
            return
        self.funname = self.statement[0: start].split()[-1]
        if self.funname.startswith('*'):
            self.funname = self.funname.split('*')[-1]


    def fun_comment(self):
        self.get_statement()
        self.get_args()
        self.get_funname()
        if not self.args:
            return

        lines = ['/**', " * %s -- " % self.funname]
        lines += [" * @%s: " % arg for arg in self.args]
        lines += [' */']

        vim.current.buffer.append(lines, self.funline)
        vim.current.window.cursor = (self.funline + 2, len(lines[1]))















