# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log as logging
import pyvim
import node
from node import Item
import vim
import copy
import utils
import frainui

def isshow(fun):
    def _fun(self, *k, **kw):
        if self.BFb and self.BFb.valid:
            if self.BFw and self.BFw.valid:
                fun(self, *k, **kw)
    return _fun

class OP_OPTIONS(object):
    @isshow
    def open(self, w):
        node = self.getnode()
        if node:
            node._open()

    @isshow
    def close(self, w):  # 关闭父级目录
        node = self.getnode()
        route = node.route()
        fa = route[-2]
        if fa == self.root:
            return # 已经是root 了, 不可以关闭

        fa._open()
        self.BFw.cursor = (fa.getlinenu(), 0)

    @isshow
    def delete(self, w):
        node = self.getnode()
        if node:
            node.FREventEmit("delete")


    def refresh(self, win=None):
        del self.BFb[:]
        self.BFb[0] = "FrainUI"
        self.nodes = {}

        self.FREventEmit("List-ReFresh-Pre")

        self.root = node.Node("root", None, self.get_roots)
        self.root.lswin = self

        self.root.node_open()

        if self.Title:
            pyvim.settitle(self.Title)

        self.FREventEmit("List-ReFresh-Post")
        self.nu_refresh += 1

class NODE(object):
    def getnode(self, linenu = None):
        if linenu == None: # 没有输入行号, 使用当前行
            line = self.BFb[self.BFw.cursor[0] - 1]
        else:
            if linenu >= len(self.BFb):
                return
            line = self.BFb[linenu]

        #line = line.decode('utf8')
        try:
            node_index = int(line.split('<|>')[1])
            logging.debug("getnode ID: %s" % node_index)

            return self.nodes.get(node_index)
        except:
            logging.debug('getnode by line [%s]: fail' % line)



import Buffer
class LIST(Buffer.BF, OP_OPTIONS, NODE):
    def __init__(self, name, get_roots, **kw):
        frainui.BF.__init__(self)
        self.FRRegister(name)

        self.names_for_find = None
        self.nu_refresh     = 0         # count the refresh
        self.get_roots      = get_roots
        self.Title          = None
        self.root           = None
        self.nodes       = {}

        def hook(buf):
            self.FREventEmit("List-Show")


        self.BFFt       = "frainuilist"
        self.BFName     = "Frain"
        self.BFWdith    = 25
        self.BFVertical = True
        self.BFVertical = kw.get("positoin", 'topleft')


        self.FREventBind("BF-Create-Post", hook)

        self.FREventBind("OP-Open",           self.open)
        self.FREventBind("OP-Close",          self.close)
        self.FREventBind("OP-Delete",         self.delete)
        self.FREventBind("OP-Refresh",        self.refresh)

        def focus(s):
            self.BFFocus()

        self.FREventBind("OP-Focus",          focus)

    def show(self):
        self.BFCreate()
        pyvim.addevent("CursorMovedI", self.update_status, self.BFb)


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
                if self.BFw != vim.current.window:
                    w = vim.current.window
                    vim.current.window = self.BFw

                vim.command('call winline()')
                if w:
                    vim.current.window = w
                return

        self.BFw.cursor = (1, 0)

    @isshow
    def update_status(self):
        node = self.getnode()
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

