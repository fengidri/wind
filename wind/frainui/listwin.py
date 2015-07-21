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

        self.root = node.Node("root", None, self.get_roots)

        #self.root = node.Node('root')

        ## hooks
        #for r in self.LS_GetRoots():
        #    self.root.append(r)

        self.root.node_open(1)

        if self.Title:
            self.settitle(self.Title)

        #self.LS_Refresh_Hook()
        self.FREventEmit("ListReFresh")
        self.nu_refresh += 1


    def focus(self):# 切换到list 窗口,
        self.win.show()

    def setnames(self, names):
        self.names_for_find = names

    def LS_Find(self, _names = None):
        """
          在 list win 中显示由_names 指定的条目
        """
        #names = copy.copy(_names)

        self.names_for_find = None
        self.FREventEmit("ListNames")
        names = self.names_for_find
        if not names: return

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

def find():
    #在NERDTree窗口中找到当前文件的位置
    """显示出当前文件的位置.
    当前是在NERDTree 中显示"""
    if vim.current.buffer.name == '':
        return -1
    if vim.current.buffer.options[ 'buftype' ] != '':
        return -1
    if pyvim.is_empty( ):
        return -1

    w = vim.current.window

    frain = LIST()
    frain.LS_Find()

    #s =
    #if s == 'NROOT':
    #    frain.add_cur_path()
    #    frain.refresh()
    #    frain.find()

    #if not s:
    #    frain.refresh()
    #    frain.find()

    vim.current.window = w
    return 0


class LIST(utils.Object, LISTOPTIONS, LISTNODS):#  list 窗口对象
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

    def __init__(self, get_roots=None):
        if hasattr(self, 'win'):
            return

        self.names_for_find = None
        self.nu_refresh = 0 # count the refresh
        self.get_roots = get_roots

        def hook(buf):
            self.FREventEmit("ListShow")

        import Buffer
        self.win = Buffer.Buffer(
                vertical = True,
                position = Buffer.TOPLEFT,
                width = 25,
                title = "Frain",  ft="frainlist")

        #self.win.Buf_New_Hook = self.LS_WinOpen_Hook
        self.win.FREventBind("BufNew", hook)
        self.win.show()

        Item.lswin = self.win

        pyvim.addevent("BufEnter", find)
        pyvim.addevent('CursorMoved', self.update_status, self.win.b)



if __name__ == "__main__":
    pass

