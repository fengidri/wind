# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-19 09:39:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import vim
import pyvim
import utils


# OP: use Options

LEFTABOVE  = "leftabove"
RIGHTBELOW = "rightbelow"
TOPLEFT    = "topleft"
BOTRIGHT   = "boright"

class options(object):
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

class Buffer(utils.Object, options):
    def __init__(self, title='',
            position = '',
            vertical=False,
            width=25,
            height=15,
            ft='fraintmp'):

        self.b = None
        self.w = None

        self.title = title
        self.Buf_Close_Hook = None

        self.ft       = ft
        self.width    = width
        self.height   = height
        self.position = position
        self.vertical = vertical

        if self.vertical:
            self.size = self.width
            self.cmd = "vnew"
        else:
            self.size = self.height
            self.cmd = "new"

        self.Buffer = self
        self.input_focus = None

    def delete(self):
        vim.command("bdelete %s"% self.b.number)
        self.b = None

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



        cmd = "{pos} {size}{cmd}".format(size = self.size,
                cmd = self.cmd,
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


            if self.Buf_Close_Hook:
               # pyvim.addevent('BufUnload', self.close_hook, '<buffer>')
                pyvim.addevent('QuitPre', self.Buf_Close_Hook, self.b)

            self.b = vim.current.buffer
            utils.Objects[self.b] = self

class BFVimEvent(object):
    def BFVimEventQuitPre(self):
        pass

    def BFVimEventWipeout(self):
        self.FREventEmit("BF-Destory")
        self.BFw = None
        self.BFb = None
        pyvim.delevent(self.vimev1)
        pyvim.delevent(self.vimev2)



            #, title='',
            #position = '',
            #vertical=False,
            #width=25,
            #height=15,
            #ft='fraintmp'):
class BF(utils.Object, BFVimEvent):
    def __init__(self):
        self.BFb = None
        self.BFw = None

        self.BFName       = ''

        self.BFFt         = "fraintmp"
        self.BFWidth      = 25
        self.BFHeight     = 15
        self.BFPosition   = ''
        self.BFVertical   = False

        self.BFInputFocus = None

    def __create_win(self):
        if self.BFVertical:
            size = self.BFWidth
            cmd = "vnew"
        else:
            size = self.BFHeight
            cmd = "new"

        cmd = "{pos} {size}{cmd} {name}".format(size = size, cmd = cmd,
                pos = self.BFPosition, name = self.BFName)

        vim.command(cmd)
        self.BFw = vim.current.window

    def BFIsShow(self, fun):
        def _fun(*k, **kw):
            if self.BFb and self.BFb.valid:
                if self.BFw and self.BFw.valid:
                    fun(*k, **kw)

        return _fun



    def BFFocus(self):
        if self.BFw and self.BFw.valid:
            vim.current.window = self.BFw
            return True

    def BFCreate(self):
        if self.BFb and self.BFb.valid:
            return

        self.FREventEmit("BF-Create-Pre")

        self.__create_win()
        if self.BFFt:
            vim.command("set ft=%s" % self.BFFt)

        self.BFb = vim.current.buffer
        self.FREventEmit("BF-Create-Post")

        self.vimev1= pyvim.addevent('QuitPre', self.BFVimEventQuitPre, self.BFb)
        self.vimev2= pyvim.addevent('BufWipeout', self.BFVimEventWipeout, self.BFb)

        utils.Objects[self.BFw] = self

    def BFShow(self):
        """显示当前 buffer 窗口 如果已经显示, 会 focus 到那个窗口 """
        if not (self.b and self.b.valid):
            self.BFCreate()
            return

        if self.BFw and self.BFw.valid:
            vim.current.window = self.BFw
            return

        self.__create_win()
        vim.command("buffer %s" % self.BFb.number)

    def BFHide(self):
        if self.BFw and self.BFw.valid:
            vim.command("%swincmd quit" % self.BFw.number)
            self.BFw = None

    def BFWipeout(self):
        if self.BFb.valid:
            vim.command("bwipeout %s" % self.BFb.number)



if __name__ == "__main__":
    pass

