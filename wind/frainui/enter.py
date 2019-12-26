# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 12:23:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from . import utils
import im
import pyvim
import vim

class EnterLineIM(im.keybase.BaseEnd):
    def cb_enter(self):
        self.enter.FREventEmit('Enter-Active')
        return True

    def cb_esc(self):
        im.async_feed('frainui', 'OP-Quit')
        return True

    def cb_tab(self):
        vim.command("set cursorline")
        im.imrc.feedkeys('\<esc>2G')
        return True


    def cb_backspace(self):
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
        self.linenu = linenu
        self.Buffer = buf

        self.col = len(prefix) + 1

        vim.Function("matchaddpos")("TODO", [[1, 1, self.col - 1]], 11)

        self.Buffer.BFb[linenu] = "%s " % prefix

        self.prefix_len = len(prefix)

        self.IM = EnterLineIM()
        self.IM.enter = self

        self.last_content = ""

        self.handle1 = pyvim.addevent("CursorMovedI", self.cursor_moved,
                self.Buffer.BFb)
        #self.handle2 = pyvim.addevent("InsertLeave", self.quit,
        #        self.Buffer.b)

        vim.current.window.cursor = (1, 999)
        vim.command("startinsert!")



    def cursor_moved(self):
        l, c = vim.current.window.cursor

        #pyvim.log.error("%s %s %s %s", self.linenu, self.col, l, c)

        #if self.linenu != l - 1 or c <= self.col:
        #    c = len(self.buf.b[self.linenu])
        #    vim.current.window.cursor = (self.linenu + 1, c)

        c = self.get_text()
        if c != self.last_content:
            self.last_content = c
            self.FREventEmit('Enter-Change')


    def get_text(self):
        c = self.Buffer.BFb[self.linenu][self.prefix_len:]
        return self.Buffer.BFb[self.linenu][self.col:]



    def delete(self):
        pyvim.delevent(self.handle1)







if __name__ == "__main__":
    pass

