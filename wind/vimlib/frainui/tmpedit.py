# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-19 09:39:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import vim
import pyvim

class TmpEdit(object):
    def __init__(self, title='TmpEdit'):
        self.title = title
        self.close_hook = None
        self.entry_hook = None

    def show(self):
        vim.command("16new " )
        vim.command("set ft=fraintmp")
        self.w = vim.current.window
        self.b = vim.current.buffer
        if self.entry_hook:
            self.entry_hook()

        if self.close_hook:
           # pyvim.addevent('BufUnload', self.close_hook, '<buffer>')
            pyvim.addevent('QuitPre', self.close_hook, '<buffer>')


if __name__ == "__main__":
    pass

