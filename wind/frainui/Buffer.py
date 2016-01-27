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


class BFVimEvent(object):
    def BFVimEventQuitPre(self):
        pass

    def BFVimEventWipeout(self):
        self.FREventEmit("BF-Destory")
        self.BFw = None
        self.BFb = None
        pyvim.delevent(self.vimev1)
        pyvim.delevent(self.vimev2)

class BF(utils.Object, BFVimEvent):
    def __init__(self):
        self.BFb = None

        self.BFName       = ''

        self.BFFt         = "fraintmp"
        self.BFWidth      = 25
        self.BFHeight     = 15
        self.BFPosition   = ''
        self.BFVertical   = False

        self.BFInputFocus = None

    @property
    def BFw(self):
        for w in vim.windows:
            if w.buffer.number == self.BFb.number:
                return w

    def __create_win(self):
        if self.BFVertical:
            size = self.BFWidth
            cmd = "vnew"
        else:
            size = self.BFHeight
            cmd = "new"

        #cmd = "{pos} {size}{cmd} {name}".format(size = size, cmd = cmd,
        #        pos = self.BFPosition, name = self.BFName)
        cmd = "{pos} {size}{cmd} ".format(size = size, cmd = cmd,
                pos = self.BFPosition)

        vim.command(cmd)

    def BFIsShow(self, fun):
        def _fun(*k, **kw):
            if self.BFb and self.BFb.valid:
                if self.BFw and self.BFw.valid:
                    fun(*k, **kw)

        return _fun


    def BFSetImFocus(self, obj):
        self.BFInputFocus = obj

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

        utils.Objects[self.BFb] = self

    def BFShow(self):
        """显示当前 buffer 窗口 如果已经显示, 会 focus 到那个窗口 """
        if not (self.BFb and self.BFb.valid):
            self.BFCreate()
            return

        if self.BFw and self.BFw.valid:
            vim.current.window = self.BFw
            return

        self.__create_win()
        vim.command("buffer %s" % self.BFb.number)

    def BFHide(self):
        if self.BFw and self.BFw.valid:
            vim.command("%swincmd q" % self.BFw.number)
            self.BFw = None
            return True

    def BFToggle(self):
        if self.BFHide():
            return
        else:
            self.BFShow()

    def BFWipeout(self):
        if self.BFb.valid:
            vim.command("bwipeout %s" % self.BFb.number)

