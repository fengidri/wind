# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-19 09:39:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import vim
import pyvim
import utils

LEFTABOVE  = "leftabove"
RIGHTBELOW = "rightbelow"
TOPLEFT    = "topleft"
BOTRIGHT   = "boright"

class Buffer(utils.Object):
    buf = None
    def __init__(self, title='', position = '',
            vertical=False, width=25, height=15, ft='fraintmp'):
        self.b = None
        self.w = None

        self.title = title
        self.Buf_Close_Hook = None
        self.Buf_New_Hook = None

        self.ft = ft

        self.width = width
        self.height = height
        self.position = position

        self.vertical = vertical

        if self.vertical:
            self.size = self.width
            self.cmd = "vnew"
        else:
            self.size = self.height
            self.cmd = "new"
        self.previous = None

        pyvim.addevent("WinLeave", self._previous)
        self.Buffer = self
        self.input_focus = None


    def _previous(self):
        self.previous = vim.current.window


    def get_cursor(self):
        return self.w.cursor

    def set_cursor(self, cursor):
        self.w.cursor = cursor

    cursor = property(get_cursor, set_cursor)

    def is_focus(self):
        return vim.current.window == self.w

    def clear(self):
        del self.b[:]

    def linenu(self):
        return len(self.b)

    def getline(self, linenu = None):
        if not linenu:
            return vim.current.line
        return self.b[linenu]

    def show(self):
        """显示当前 buffer 窗口
        如果已经显示, 会 focus 到那个窗口
        """
        buf_back = None
        if self.b and self.b.valid:
            if self.w and self.w.valid:
                vim.current.window = self.w
                return
            else:
                buf_back = "buffer %s" % self.b.number



        cmd = "{pos} {size}{cmd} {file}".format(size = self.size,
                cmd = self.cmd, file=self.title,
                pos = self.position)

        vim.command(cmd)
        self.w = vim.current.window

        if buf_back:
            vim.command(buf_back)
            return
        else:
            if self.ft:
                vim.command("set ft=%s" % self.ft)

            self.FREventEmit("BufNew")

            #if self.Buf_New_Hook:
            #    self.Buf_New_Hook()

            if self.Buf_Close_Hook:
               # pyvim.addevent('BufUnload', self.close_hook, '<buffer>')
                pyvim.addevent('QuitPre', self.Buf_Close_Hook, self.b)

            self.b = vim.current.buffer
            utils.Objects[self.b] = self



if __name__ == "__main__":
    pass

