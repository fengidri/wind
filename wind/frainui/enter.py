# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 12:23:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import utils
import im
import pyvim
import vim

class EnterLineIM(im.keybase.BaseEnd)
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
        im.keybase.BaseEnd.__init__(self)

        prefix = "\\green;%s\\end;" % prefix

        self.buf = buf
        self.linenu = linenu
        self.buf.b[linenu] = prefix
        self.col = len(prefix)

        self.Buffer = buf
        self.IM = EnterLine()







if __name__ == "__main__":
    pass

