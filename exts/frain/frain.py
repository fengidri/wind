# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:44:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from frainui import LIST
import frainui
import libpath
import vim
import pyvim
import utils
import os
import helper
from pyvim import log

from project import Project

BufNewFile = {}
################################################################################

class Events(object):
    def del_root_handle(self, node):
        for p in Project.All:
            if p.root == node.ctx:
                p.close()
                self.listwin.refresh()

    def FrainListGetRootsHook(self, node):
        pyvim.Roots = []  # 整个vim 可用的变量

        if vim.vars.get("frain_buffer", 0) == 1:
            dp = r"\green;Buffers\end;"
            root = frainui.Node("Buffers", None, get_buffers, dp)
            self.buf_node = root
            node.append(root)

        for p in Project.All:
            pyvim.Roots.append(p.root)
            root = frainui.Node(p.name, p.root, get_child)
            root.FREventBind("delete", self.del_root_handle)

            node.append(root)

class FrainList(Events):
    def __init__(self):
        self.buf_node = None

        frain.origin_window_title = pyvim.gettitle()

        self.listwin = LIST("frain", self.FrainListGetRootsHook)

        self.listwin.FREventBind("List-ReFresh-Post", FrainListRefreshHook)
        self.listwin.FREventBind("List-ReFresh-Pre",  FrainListRefreshPreHook)
        self.listwin.FREventBind("List-Show",         FrainListShowHook)

        self.listwin.show()
        pyvim.addevent("BufEnter",   helper.BufEnter)
        pyvim.addevent("BufNewFile", self.bufnewfile)
        pyvim.addevent("BufNew",     self.bufnew)

    def bufnew(self):
        if self.buf_node:
            self.buf_node.refresh()

    def bufnewfile(self):
        path = vim.current.buffer.name
        log.error("bufnewfile buttype: %s.", vim.current.buffer.options['buftype'])
        if vim.current.buffer.options['buftype'] != '':
            return
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        if BufNewFile.get(dirname):
            BufNewFile.get(dirname).append(basename)
        else:
            BufNewFile[dirname] = [basename]


    #def add_cur_path(self):
    #    path = utils.bufferpath()
    #    self.add(path, '')

    #def cur_project(self):
    #    "返回当前 bufferf 所有在 project 对象"
    #    path = utils.bufferpath()
    #    for p in Project.All:
    #        if path.startswith(p.root):
    #            return p


class frain(object):
    origin_window_title = None

if __name__ == "__main__":
    pass

