# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import node
from node import Item
import vim
import logging
import copy
import pyvim
class LISTHOOK(object):
    def LS_WinOpen_Hook(self):
        "事件: 窗口创建"
        pass

    def LS_GetRoots(self):
        "返回 roots"
        pass

    def LS_Refresh_Hook(self):
        "事件: 刷新"
        pass

class LISTOPTIONS(object):
    def open(self):
        l, c = vim.current.window.cursor
        node = Item.getnode()
        node._open(l)

    def close(self):  # 关闭父级目录
        node = Item.getnode()
        route = node.route()
        fa = route[-2]
        if fa == self.root:
            return # 已经是root 了, 不可以关闭

        linenu = self.getlinenu(fa)
        fa._open(linenu)
        self.win.cursor = (linenu, 0)


    def refresh(self):
        self.win.clear()
        self.win.b[0] = "FrainUI"
        Item.nodes = {}
        self.root = node.Node('root')

        # hooks
        for r in self.LS_GetRoots():
            self.root.append(r)

        self.root.opened = False
        self.root.node_open(1)

        if self.Title:
            self.settitle(self.Title)

        self.LS_Refresh_Hook()


    def focus(self):# 切换到list 窗口,
        self.win.show()

    def LS_Find(self, _names):
        """
          在 list win 中显示由_names 指定的条目
        """
        names = copy.copy(_names)

        names.insert(0, 'root')
        logging.error('names: %s', names)

        leaf = self.root.find(names)
        if not leaf:
            self.win.cursor = (1, 0)
            return False

        route = leaf.route()
        if not route:
            self.win.cursor = (1, 0)
            return False

        w = None
        if vim.current.window != self.win.w:
            w = vim.current.window
            vim.current.window = self.win.w

        logging.error('route: %s', route)
        for n in route[1:-1]:
            n.node_open(self.getlinenu(n))

        linenu = self.getlinenu(route[-1])
        self.win.cursor = (linenu, 0)
        self.update_status()
        vim.command('normal zz')

        if w:
            vim.current.window = w

        return True

    def update_status(self):
        node = Item.getnode()
        if not node:
            return

        route = node.route()
        if not route:
            return

        path = '/'.join([r.name for r in route[1:]])
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


class LIST(LISTHOOK, LISTOPTIONS, LISTNODS):#  list 窗口对象
    Title = None
    @staticmethod
    def get_instance():
        if hasattr(LIST, '_instance'):
            return LIST._instance

    def __new__(cls, *args, **kw):
        if not hasattr(LIST, '_instance'):
            orig = super(LIST, cls)
            LIST._instance = orig.__new__(cls, *args, **kw)
        return LIST._instance

    def __init__(self):
        """
            self.root(Node:root)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
        """
        if hasattr(self, 'win'):
            return
        import Buffer
        self.win = Buffer.Buffer(
                vertical = True,
                position = Buffer.TOPLEFT,
                width = 25,
                title = "Frain",  ft="frainlist")

        self.win.Buf_New_Hook = self.LS_WinOpen_Hook
        self.win.show()

        Item.lswin = self.win

        pyvim.addevent('CursorMoved', self.update_status, self.win.b)



if __name__ == "__main__":
    pass

