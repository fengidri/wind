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
        self.enter.FREventEmit('active')
        im.imrc.feedkeys('\<esc>')
        return True

    def cb_backspace(self):
        pyvim.log.error('cb_bs')
        l, c = vim.current.window.cursor

        if c == self.enter.col:
            pass

        elif c < self.enter.col:
            vim.current.window.cursor = (l, self.enter.col)

        else:
            im.imrc.feedkeys('\<bs>')
        return True


class EnterLine(utils.Object):
    def __init__(self, buf, linenu, prefix = ''):

        self.buf = buf
        self.linenu = linenu


        #prefix = "\\red;%s\\end;" % prefix

        self.col = len(prefix)

        vim.Function("matchaddpos")("TODO", [[1, 1, self.col]], 11)

        self.buf.b[linenu] = "%s " % prefix

        self.prefix_len = len(prefix)

        self.Buffer = buf
        self.IM = EnterLineIM()
        self.IM.enter = self

        self.last_content = ""

        self.handle1 = pyvim.addevent("CursorMovedI", self.cursor_moved, self.buf.b)
        self.handle2 = pyvim.addevent("InsertLeave", self.quit, self.buf.b)

        vim.current.window.cursor = (1, 999)
        vim.command("startinsert!")

        pyvim.log.error("enter init: %s", id(self.buf.b))

    def quit(self):
        self.FREventEmit('quit')

    def cursor_moved(self):
        l, c = vim.current.window.cursor

        #pyvim.log.error("%s %s %s %s", self.linenu, self.col, l, c)

        #if self.linenu != l - 1 or c <= self.col:
        #    c = len(self.buf.b[self.linenu])
        #    vim.current.window.cursor = (self.linenu + 1, c)

        c = self.get_content()
        if c != self.last_content:
            self.last_content = c
            self.FREventEmit('change', c)


    def get_content(self):
        c = self.buf.b[self.linenu][self.prefix_len:]
        pyvim.log.error("enter content: %s", c)

        return self.buf.b[self.linenu][self.col:].strip()



    def delete(self):
        pyvim.delevent(self.handle1)
        pyvim.delevent(self.handle2)







if __name__ == "__main__":
    pass

