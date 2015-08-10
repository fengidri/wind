# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import node
from node import Item
import vim
from pyvim import log as logging
import copy
import pyvim
import utils
import frainui

class LISTOPTIONS(object):
    def open(self, win):
        node = Item.getnode()
        if node:
            node._open()

    def close(self, win):  # 关闭父级目录
        node = Item.getnode()
        route = node.route()
        fa = route[-2]
        if fa == self.root:
            return # 已经是root 了, 不可以关闭

        fa._open()
        self.win.cursor = (fa.getlinenu(), 0)

    def delete(self, win):
        node = Item.getnode()
        if node:
            node.FREventEmit("delete")

    def focus(self, win):
        win.show()

    def refresh(self, win=None):
        self.win.clear()
        self.win.b[0] = "FrainUI"
        Item.nodes = {}

        self.FREventEmit("ListReFreshPre")

        Item.clear() # 在刷新的时候, 把旧的所有 nodes 释放掉
        self.root = node.Node("root", None, self.get_roots)

        self.root.node_open()

        if self.Title:
            pyvim.settitle(self.Title)

        #self.LS_Refresh_Hook()
        self.FREventEmit("ListReFreshPost")
        self.nu_refresh += 1
        #self.find()

    def find(self, names):
        """
          在 list win 中显示由 names 指定的条目
          使用 names 指定 item 而不是通过, 在全局nodes 里查找node 的原因:
            1. frainui 对于子节点的生成是在用户打开节点里的时候才获取地.
                如果进行全局性地查找是找不到的
            2.
        """

        if not names: return
        if not self.root: return

        node = self.root
        for name in names:
            subnode = node.get(name)
            if not subnode:
                node.node_close()
                node.need_fresh = True
                node.node_open()
                subnode = node.get(name)
                if not subnode:
                    break
            else:
                node.node_open()
            node = subnode
        else:
            if subnode:

                self.win.cursor = (subnode.getlinenu(), 0)
                self.update_status()

                w = None
                if self.win.w != vim.current.window:
                    w = vim.current.window
                    vim.current.window = self.win.w

                vim.command('normal zz')
                if w:
                    vim.current.window = w
                return

        self.win.cursor = (1, 0)






    def update_status(self):
        node = Item.getnode()
        if not node:
            return

        route = node.route()
        if not route:
            return

        try:
            ps = route[1:-1]
            path = '/'.join([r.name for r in ps])
        except:
            path = route[1].name
        self.win.b.vars['frain_status_path'] = path

    def settitle(self, name):#设置vim 窗口的title
        # 如果没有设置name, 则使用第一个root的name
        vim_title = name.replace( ' ', '\\ ')
        vim.command( "set title titlestring=%s" % vim_title )

class LISTNODS(object):
    def getroots(self):
        return self.root.sub_nodes

class LIST(utils.Object, LISTOPTIONS, LISTNODS):#  list 窗口对象
    def __init__(self, name, get_roots, **kw):
        self.FRRegister(name)
        self.names_for_find = None
        self.nu_refresh     = 0         # count the refresh
        self.get_roots      = get_roots
        self.Title          = None
        self.root           = None

        def hook(buf):
            self.FREventEmit("ListShow")

        import Buffer
        if not kw.get("position"):
            kw["position"] = Buffer.TOPLEFT

        self.win = Buffer.Buffer(
                vertical = True,
                width = 25,
                title = "Frain",
                ft="frainuilist", **kw)

        self.win.FREventBind("BufNew",  hook)
        self.win.FREventBind("open",    self.open)
        self.win.FREventBind("close",   self.close)
        self.win.FREventBind("delete",  self.delete)
        self.win.FREventBind("refresh", self.refresh)

        self.FREventBind("focus",   self.focus)


    def show(self):
        self.win.show()
        Item.lswin = self.win
        pyvim.addevent('CursorMoved', self.update_status, self.win.b)

    def close(self):
        self.win.delete()

def isshow(fun):
    def _fun(self, *k, **kw):
        if self.BFb and self.BFb.valid:
            if self.BFw and self.BFw.valid:
                fun(self, *k, **kw)
    return _fun


class _LILST(frainui.BF):
    def __init__(self, name, get_roots, **kw):
        frainui.BF.__init__(self)
        self.FRRegister(name)

        self.names_for_find = None
        self.nu_refresh     = 0         # count the refresh
        self.get_roots      = get_roots
        self.Title          = None
        self.root           = None

        def hook(buf):
            self.FREventEmit("ListShow")


        self.BFFT       = "frainuilist"
        self.BFName     = "Frain"
        self.BFWdith    = 25
        self.BFVertical = True
        self.BFVertical = kw.get("positoin", 'topleft')


        self.FREventBind("BF-Create-Post", hook)

        self.FREventBind("OP-Open",           self.open)
        self.FREventBind("OP-Close",          self.close)
        self.FREventBind("OP-Delete",         self.delete)
        self.FREventBind("OP-Refresh",        self.refresh)

        self.FREventBind("OP-Focus",          self.BFFocus)

    def show(self):
        self.BFCreate()
        pyvim.addevent("CursorMovedI", self.update_status, self.BFb)

    @isshow
    def open(self, w):
        node = Item.getnode()
        if node:
            node._open()

    @isshow
    def close(self, w):  # 关闭父级目录
        node = Item.getnode()
        route = node.route()
        fa = route[-2]
        if fa == self.root:
            return # 已经是root 了, 不可以关闭

        fa._open()
        self.BFw.cursor = (fa.getlinenu(), 0)

    @isshow
    def delete(self, w):
        node = Item.getnode()
        if node:
            node.FREventEmit("delete")


    def refresh(self, win=None):
        del self.BFb[:]
        self.BFb.b[0] = "FrainUI"
        Item.nodes = {}

        self.FREventEmit("ListReFreshPre")

        Item.clear() # 在刷新的时候, 把旧的所有 nodes 释放掉
        self.root = node.Node("root", None, self.get_roots)

        self.root.node_open()

        if self.Title:
            self.settitle(self.Title)

        self.FREventEmit("ListReFreshPost")
        self.nu_refresh += 1

    @isshow
    def find(self, names):
        """
          在 list win 中显示由 names 指定的条目
          使用 names 指定 item 而不是通过, 在全局nodes 里查找node 的原因:
            1. frainui 对于子节点的生成是在用户打开节点里的时候才获取地.
                如果进行全局性地查找是找不到的
            2.
        """

        if not names: return
        if not self.root: return

        node = self.root
        for name in names:
            subnode = node.get(name)
            if not subnode:
                node.node_close()
                node.need_fresh = True
                node.node_open()
                subnode = node.get(name)
                if not subnode:
                    break
            else:
                node.node_open()
            node = subnode
        else:
            if subnode:

                self.BFw.cursor = (subnode.getlinenu(), 0)
                self.update_status()

                w = None
                if self.BFw.w != vim.current.window:
                    w = vim.current.window
                    vim.current.window = self.BFw.w

                vim.command('normal zz')
                if w:
                    vim.current.window = w
                return

        self.BFw.cursor = (1, 0)






    @isshow
    def update_status(self):
        node = Item.getnode()
        if not node:
            return

        route = node.route()
        if not route:
            return

        try:
            ps = route[1:-1]
            path = '/'.join([r.name for r in ps])
        except:
            path = route[1].name
        self.BFb.vars['frain_status_path'] = path





if __name__ == "__main__":
    pass

