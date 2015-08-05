# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 12:23:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import utils
import im
import pyvim
import vim

class EnterLineIM(im.keybase.BaseEnd):
    def cb_enter(self):
        pyvim.log.error('cb_enter')
        self.FREventEmit('enter_active')
        return True

    def cb_backspace(self):
        pyvim.log.error('cb_bs')
        l, c = vim.current.window.cursor

        if c == self.col:
            pass

        elif c < self.col:
            vim.current.window.cursor = (l, self.col)

        else:
            im.imrc.feedkeys('\<bs>')
        return True


class EnterLine(utils.Object):
    def __init__(self, buf, linenu, prefix = ''):
        prefix = "\\green;%s\\end;" % prefix

        self.buf = buf
        self.linenu = linenu
        self.buf.b[linenu] = prefix
        self.col = len(prefix)

        self.Buffer = buf
        self.IM = EnterLineIM()
        self.IM.col = self.col

        self.last_content = ""
        pyvim.addevent("CursorMovedI", self.cursor_moved, self.buf.b)

    def cursor_moved(self):
        l, c = vim.current.window.cursor
        if self.linenu != l - 1 or c <= self.col:
            c = len(self.buf.b[self.linenu])
            vim.current.window.cursor = (self.linenu + 1, c)

        c = self.get_content()
        if c != self.last_content:
            self.last_content = c
            self.FREventEmit('change', c)


    def get_content(self):
        c = self.buf.b[self.linenu][self.col:]
        pyvim.log.error("enter content: %s", c)

        return self.buf.b[self.linenu][self.col:]










if __name__ == "__main__":
    pass

