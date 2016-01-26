# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:44:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from frainui import LIST

import pyvim

import helper_listwin
import helper_vim

class FrainList(object):
    def __init__(self):
        self.buf_node = None
        self.new_files = {}

        self.origin_window_title = pyvim.gettitle()

        listwin = LIST("frain", helper_listwin.FrainListGetRootsHook)

        listwin.FREventBind("List-ReFresh-Post",
                helper_listwin.FrainListRefreshHook)

        listwin.FREventBind("List-ReFresh-Pre",
                helper_listwin.FrainListRefreshPreHook)


        pyvim.addevent("BufEnter",   helper_vim.BufEnter,   arg = (self,))
        pyvim.addevent("BufNewFile", helper_vim.BufNewFile, arg = (self,))
        pyvim.addevent("BufNew",     helper_vim.BufNew,     arg = (self,))
        pyvim.addevent('VimLeave',   helper_vim.VimLeave,   arg = (self,))

        listwin.frain = self

        listwin.show()

        self.listwin = listwin

