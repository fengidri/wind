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

class LISTOPTIONS(object):
    def open(self, win):
        l, c = vim.current.window.cursor
        node = Item.getnode()
        if node:
            node._open(l)

    def close(self, win):  # 关闭父级目录
        node = Item.getnode()
        route = node.route()
        fa = route[-2]
        if fa == self.root:
            return # 已经是root 了, 不可以关闭

        linenu = self.getlinenu(fa)
        fa._open(linenu)
        self.win.cursor = (linenu, 0)

    def delete(self, win):
        l, c = vim.current.window.cursor
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

        #self.root = node.Node('root')

        ## hooks
        #for r in self.LS_GetRoots():
        #    self.root.append(r)

        self.root.node_open(1)

        if self.Title:
            self.settitle(self.Title)

        #self.LS_Refresh_Hook()
        self.FREventEmit("ListReFreshPost")
        self.nu_refresh += 1
        #self.find()

    def show_item(self, item):
        route = item.route()
        if not route:
            self.win.cursor = (1, 0)
            return False

        w = None
        if vim.current.window != self.win.w:
            w = vim.current.window
            vim.current.window = self.win.w

        ############## start

        for n in route[1:-1]:
            n.node_open(self.getlinenu(n))

        linenu = self.getlinenu(route[-1])
        self.win.cursor = (linenu, 0)

        self.update_status()
        vim.command('normal zz')
        ############## start

        if w:
            vim.current.window = w
        return True

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

        names.insert(0, 'root')

        leaf = self.root.find(names)
        if not leaf:
            self.win.cursor = (1, 0)
            logging.error('@@@@@@@ find leaf false')
            return False

        return self.show_item(leaf)


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
    def getlinenu(self, node):
        num = 0
        for linenu, line in enumerate(self.win.b):
            try:
                ID = int(line.split('<|>')[1])
                if ID == node.ID:
                    num = linenu
                    break
            except:
                pass
        return num + 1

    def getroots(self):
        return self.root.sub_nodes

class LIST(utils.Object, LISTOPTIONS, LISTNODS):#  list 窗口对象
    def __init__(self, name, get_roots):
        self.FRRegister(name)
        self.names_for_find = None
        self.nu_refresh     = 0         # count the refresh
        self.get_roots      = get_roots
        self.Title          = None
        self.root           = None

        def hook(buf):
            self.FREventEmit("ListShow")

        import Buffer
        self.win = Buffer.Buffer(
                vertical = True,
                position = Buffer.TOPLEFT,
                width = 25,
                title = "Frain",
                ft="frainlist")

        self.win.FREventBind("BufNew",  hook)
        self.win.FREventBind("open",    self.open)
        self.win.FREventBind("close",   self.close)
        self.win.FREventBind("delete",  self.delete)
        self.win.FREventBind("focus",   self.focus)
        self.win.FREventBind("refresh", self.refresh)



    def show(self):
        self.win.show()
        Item.lswin = self.win
        pyvim.addevent('CursorMoved', self.update_status, self.win.b)




if __name__ == "__main__":
    pass

