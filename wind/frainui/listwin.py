# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log as logging
import pyvim
from . import node
import vim
import copy
from . import utils
import frainui
from . import g

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
            node.FREventEmit("delete", self)


    def refresh(self, win=None, opensub = False):
        current = self.getnode()
        if current:
            names = current.names()
        else:
            names = None

        del self.BFb[:]

        self.lines = []
        self.lines.append(self.title)
        self.nodes = {}

        self.FREventEmit("List-ReFresh-Pre")

        self.root = node.Node("root", None, self.get_roots)
        self.root.lswin = self
        self.root.root = self.root

        self.root.node_open(opensub, 0, isroot = True)

        self.BFb[0] = self.title
        del self.lines[0]
        self.BFb.append(self.lines)
        self.lines = None

        self.FREventEmit("List-ReFresh-Post")
        self.nu_refresh += 1

        if names:
            self.find(names)


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
            node_index = int(line.split(',', 1)[0])
            logging.debug("getnode ID: %s" % node_index)

            return self.nodes.get(node_index)
        except:
            logging.debug('getnode by line [%s]: fail' % line)

def BufEnter(_):
    num = vim.current.buffer.number

    leaf = g.buf_leaf_map.get(num)
    if not leaf:
        return

    lswin = leaf.lswin
    lswin.focus(leaf)


from . import Buffer
class LIST(Buffer.BF, OP_OPTIONS, NODE):
    def __init__(self, name, get_roots,
                 position = 'topleft',
                 use_current_buffer= False,
                 ft = "frainuilist",
                 title = 'FrainUI',
                 autofocus = True):
        """
            autofocus just work for, all buffer opened by frain.
            If user can open buffer, then this buffer cannot found by
            autofocus.
        """
        if not g.buf_enter_event and autofocus:
            g.buf_enter_event = True
            pyvim.addevent("BufEnter", BufEnter, arg = (None,))

        frainui.BF.__init__(self)
        node.LIST = self

        self.lines = []

        self.FRRegister(name)

        self.names_for_find = None
        self.nu_refresh     = 0         # count the refresh
        self.get_roots      = get_roots
        self.root           = None
        self.nodes       = {}

        def hook(buf):
            self.FREventEmit("List-Show")

        self.title = title

        self.BFFt       = ft
        self.BFName     = "Frain"
        self.BFWdith    = 25
        self.BFVertical = True
        self.BFVertical = position


        self.FREventBind("BF-Create-Post", hook)

        self.FREventBind("OP-Open",           self.open)
        self.FREventBind("OP-Close",          self.close)
        self.FREventBind("OP-Delete",         self.delete)
        self.FREventBind("OP-Refresh",        self.refresh)

        def focus(s):
            self.BFFocus()

        self.FREventBind("OP-Focus",          focus)
        self.use_current_buffer = use_current_buffer

    def show(self):
        self.BFCreate(use_current = self.use_current_buffer)
        pyvim.addevent("CursorMovedI", self.update_status, self.BFb)

    @isshow
    def focus(self, leaf):
        if not self.root: return

        ns = []
        n = leaf.father
        while n:
            ns.append(n)
            n = n.father

        for n in ns:
            n.node_open()

        l = leaf.getlinenu()

        if l == None:
            return

        self.BFw.cursor = (l, 0)
        self.update_status()

        w = None
        if self.BFw != vim.current.window:
            w = vim.current.window
            vim.current.window = self.BFw

        #在 list 窗口中显示当前行
        vim.command('call winline()')
        #vim.command('normal zs')
        if w:
            vim.current.window = w

    @isshow
    def find(self, names):
        """
          在 list win 中显示由 names 指定的条目
          使用 names 指定 item 而不是通过, 在全局nodes 里查找node 的原因:
            1. frainui 对于子节点的生成是在用户打开节点里的时候才获取地.
                如果进行全局性地查找是找不到的
            2.
        """

        logging.error("find: %s" % names)

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

        if node and node != self.root:
            self.BFw.cursor = (node.getlinenu(), 0)
            self.update_status()

            w = None
            if self.BFw != vim.current.window:
                w = vim.current.window
                vim.current.window = self.BFw

            #在 list 窗口中显示当前行
            vim.command('call winline()')
            #vim.command('normal zs')
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

    def append(self, line, index = None):
        if self.lines == None:
            self.BFb.append(line, index + 1)
            return

        if index:
            self.lines.insert(index + 1, line)
        else:
            self.lines.append(line)

    def getline(self, index):
        if self.lines == None:
            return self.BFb[index]

        return self.lines[index]

    def setline(self, index, line):
        if self.lines == None:
            self.BFb[index] = line
            return

        self.lines[index] = line




























