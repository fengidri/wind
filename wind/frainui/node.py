# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:28:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log as logging
import vim
import pyvim
from . import utils
from . import g

LIST = None

class Item(utils.Object):# Node与Leaf 的父类
    ID = 0
    def __init__(self):
        self.lswin   = None # 指向list.win对象.
        self.level   = 0
        self.father  = None  # 指向father 对象
        self.root    = None
        self.last_win = None

        # 从 frainui listwin 的 line 得到 item 时, 要依赖于这个索引.
        self.ID      = 0

    def bfb_getlinenu(self):
        if not self.lswin.lines:
            lines = self.lswin.BFb
        else:
            return

        for linenu, line in enumerate(lines):
            try:
                ID = int(line.split(',', 1)[0])
                if ID == self.ID:
                    return linenu + 1
            except:
                pass


    def getlinenu(self):
        if self.lswin.lines:
            lines = self.lswin.lines
        else:
            lines = self.lswin.BFb

        for linenu, line in enumerate(lines):
            try:
                ID = int(line.split(',', 1)[0])
                if ID == self.ID:
                    return linenu + 1
            except:
                pass



    def find(self, names):
        " 查找一个节点, 目标如['etc', 'nginx', 'conf.d']"
        # 好喜欢这个函数啊!! 哈哈, good
        if self.level >= len(names):#超出层级了
            return

        if self.name != names[self.level]:# 当前不节点是节查找中的一个节点
            return

        if self.level == len(names) -1 : # 当前节点是是节查找的最后一个
            return self

        if not hasattr(self, 'sub_nodes'): # 如果是leaf 直接返回
            return

        # 这个处理是针对于node 节点的
        self._get_child()

        for n in self.sub_nodes: # node 在子节点中找
            m = n.find(names)
            if m:
                return m
        else:
            logging.error('refind: %s', self.name)
            self.need_fresh = True
            self._get_child()
            for n in self.sub_nodes: # node 在子节点中找
                logging.error(n.name)
                m = n.find(names)
                if m:
                    return m


    def route(self):
        # 返回从最高层, 到本节点的路径中的所有的节点(包括自身)
        # 又是一个好函数
        rt = [self]
        fa = self.father
        while fa:
            rt.insert(0, fa)
            fa = fa.father
        return rt

class Node(Item):
    def __init__(self, name, ctx=None, get_child=None, display=None,
                isdir = True, defopen = False, prefix = ''):
        Item.__init__(self)
        self.is_node    = True
        self.sub_nodes  = []
        self.name       = name
        self.display    = display
        self.opened     = False
        self.ctx        = ctx
        self.need_fresh = True      # opened or not
        self.get_child  = get_child
        self.isdir      = isdir
        self.defopen    = defopen  # default open
        self.prefix     = prefix

    def append(self, node):
        Item.ID += 1

        node.level = self.level + 1 # 用于方便得到层级关系
        node.father = self # 子node 要记录自己的father
        node.lswin = self.lswin
        node.ID = Item.ID
        node.root = self.root

        self.lswin.nodes[Item.ID] = node

        self.sub_nodes.append(node)

    def get(self, name):
        for n in self.sub_nodes:
            if n.name == name:
                return n

    def refresh(self):
        self.need_fresh = True
        if self.opened:
            cursor = self.lswin.BFw.cursor
            self.node_close()
            self.node_open()
            self.lswin.BFw.cursor = cursor


    def show(self):
        if self.display:
            dp = self.display
        else:
            dp = self.name

        if self.opened:
            flag = '-'
        else:
            flag = '+'

        if self.isdir:
            suffix = '/'
            indent = "  " * (self.level  -1)
        else:
            indent = ''
            suffix = ''

        return "{ID},{indent}{prefix}{flag}{display}{suffix}".format(
                ID = self.ID,
                indent = indent,
                prefix = self.prefix,
                flag = flag,
                display = dp,
                suffix = suffix)

    def update(self, display, prefix = None):
        if self.prefix:
            self.prefix = prefix
        self.display = display

        linenu = self.getlinenu()
        if linenu == None:
            return

        self.lswin.setline(linenu - 1, self.show())

    def _open(self): # 回车 TODO

        if self.opened:
            self.node_close()
        else:
            self.node_open()

    def _get_child(self):
        if self.need_fresh and self.get_child:
            del self.sub_nodes[:]
            self.need_fresh = False
            self.get_child(self, LIST)

    def node_open(self, opensub = False, index = None, isroot = False):
        if self.opened: return

        self.opened = True

        if index == None:
            index = self.getlinenu() - 1

        # index is the current node index

        self._get_child()

        if not isroot:
            line = self.lswin.getline(index)
            line = line.replace('+', '-', 1)
            self.lswin.setline(index, line)

        for n in self.sub_nodes:
            # add new node after the current index
            self.lswin.append(n.show(), index)
            index += 1
            if n.is_node:
                n.opened = False
                if opensub or n.defopen:
                    index = n.node_open(True, index)

        return index



    def node_close(self): #
        if not self.opened: return
        self.opened = False

        linenu = self.getlinenu()

        buf = self.lswin.BFb
        buf[linenu - 1] = buf[linenu - 1].replace('-', '+', 1)

        start = linenu
        while True:
            node = self.lswin.getnode(linenu)
            if not node:
                break
            if node.level <= self.level:
                break
            linenu += 1

        end  = linenu

        if end > start:
            del self.lswin.BFb[start: end]


class Leaf(Item):
    def __init__(self, name, ctx=None, handle=None,
            display=None, win=None, new_win=False, last_win = False, noindent = False):
        Item.__init__(self)
        self.is_node = False
        self.name    = name
        self.display = display
        self.ctx     = ctx
        self.handle  = handle
        self.win = win
        self.new_win = new_win
        self.last_win = last_win
        self.noindent = noindent

    def show(self):
        if self.display:
            dp = self.display
        else:
            dp = self.name

        if self.noindent:
            return "%s,%s" % (self.ID, dp)
        else:
            return "%s,%s %s" % (self.ID, "  " * (self.level  -1), dp)


    def node_open(self):
        self._open()

    def _open(self):#TODO
        if not self.handle:
            return

        cmd = "vertical rightbelow new"

        while True:
            if self.new_win:
                vim.command(cmd)
                break

            if self.last_win:
                if self.root.last_win:
                    if not self.root.last_win.valid:
                        self.root.last_win = None
                        vim.command(cmd)
                    else:
                        n = self.root.last_win.buffer.number
                        if n in g.buf_leaf_map:
                            del g.buf_leaf_map[n]
                        vim.current.window = self.root.last_win
                else:
                        vim.command(cmd)
                break

            if self.win:
                if not self.win.valid:
                    self.win = None
                    continue

                break

            win = pyvim.previous()
            if win and win.valid:
                n = win.buffer.number
                if n in g.buf_leaf_map:
                    del g.buf_leaf_map[n]
                vim.current.window = win
                break

            vim.command(cmd)

        self.root.last_win = vim.current.window
        self.handle(self, LIST)
        g.buf_leaf_map[vim.current.buffer.number] = self

    def update(self, display):
        self.display = display

        linenu = self.getlinenu()
        self.lswin.BFb[linenu - 1] = self.show()


