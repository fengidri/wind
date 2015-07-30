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
from pyvim import log

from project import Project
from white_black import black_filter_files, sorted_by_expand_name

def leaf_handle(leaf):
    log.debug('leaf_handle: %s', leaf.ctx)
    vim.command( "update")
    path = libpath.pull(leaf.ctx)
    if not path:
        return
    vim.command( "e %s" % path )

def get_child(Node):
    path = Node.ctx
    log.error("get child path: %s", path)

    dirs, names = libpath.listdir(path)
    if dirs == None:
        return []

    names = black_filter_files(names)
    names = sorted_by_expand_name(names)

    dirs  = sorted(black_filter_files(dirs))


    for n in names:
        p = libpath.join(path, n)
        Node.append(frainui.Leaf(n, p, leaf_handle))

    for d in dirs:
        p = libpath.join(path, d)
        Node.append(frainui.Node(d, p, get_child))

def get_buffers(Node):
    names = []
    for b in vim.buffers:
        p = b.name
        if not p:
            continue

        if b.options['buftype'] != '':
            continue

        names.append(p)
    names.sort()
    for p in names:
        Node.append(frainui.Leaf(libpath.basename(p), p, leaf_handle))
    Node.need_fresh = True

def FrainListShowHook(listwin):
    def vimleave():
        Project.emit("FrainLeave")

    pyvim.addevent('BufWritePost', libpath.push)
    pyvim.addevent('VimLeave',  vimleave)

def FrainListRefreshHook(listwin):
    if listwin.nu_refresh == 0:
        listwin.first_fresh = False
        Project.emit("FrainEntry")
        return

def FrainListRefreshPreHook(listwin):
    if not Project.All:
        listwin.Title = 'Frain'
        return

    p = Project.All[0]
    gitinfo = p.gitinfo
    if not gitinfo:
        listwin.Title = p.name
    else:
        listwin.Title = "%s(%s)" % (p.name, gitinfo["branch"])




def FrainListGetNames(listwin):
    """显示当前的 buffer 对应的文件在 win list 中的位置

    如果, buffer 不属于任何一个 project, 返回 `NROOT'

    之后生成当前 buffer 在 win list 中的 url, 由 win list 进行查询.
    """
    path = utils.bufferpath()
    if not path:
        return

    for p in Project.All:
        if path.startswith(p.root):
            break
    else:
        return
        return 'NROOT' # not found root

    names = utils.getnames(p.root, path)
    listwin.setnames(names)

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
            root = frainui.Node("Buffers", None, get_buffers)
            node.append(root)

        for p in Project.All:
            pyvim.Roots.append(p.root)
            root = frainui.Node(p.name, p.root, get_child)
            root.FREventBind("delete", self.del_root_handle)

            node.append(root)

class FrainList(Events):
    @classmethod
    def get_instance(cls):
        if hasattr(cls, '_instance'):
            return cls._instance


    def __new__(cls, *args, **kw):
        if not hasattr(FrainList, '_instance'):
            orig = super(FrainList, cls)
            FrainList._instance = orig.__new__(cls, *args, **kw)
        return FrainList._instance

    def __init__(self):
        if hasattr(self, 'listwin'):
            return

        self.listwin = LIST("frain", self.FrainListGetRootsHook)
        self.listwin.FREventBind("ListReFreshPost",    FrainListRefreshHook)
        self.listwin.FREventBind("ListReFreshPre", FrainListRefreshPreHook)
        self.listwin.FREventBind("ListShow",       FrainListShowHook)
        self.listwin.FREventBind("ListNames",      FrainListGetNames)

        self.listwin.show()

    def add(self, path, name = ''):
        "增加一个新的 project, 提供参数 path, name"
        path = libpath.realpath(path)
        if not path:
            return
        if not name:
            name = libpath.basename(path)
        if path:
            Project(path, name)


        self.listwin.refresh()

    def add_cur_path(self):
        path = utils.bufferpath()
        self.add(path, '')

    def cur_project(self):
        "返回当前 bufferf 所有在 project 对象"
        path = utils.bufferpath()
        for p in Project.All:
            if path.startswith(p.root):
                return p

if __name__ == "__main__":
    pass

