# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:44:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from frainui import LIST
from frainui import Node, Leaf
import libpath
import logging
import vim
import pyvim
import utils
import os
from project import Project
from white_black import black_filter_files, sorted_by_expand_name

class FrainListSub(LIST):
    first_fresh = True
    def LS_GetRoots(self):
        pyvim.Roots = []  # 整个vim 可用的变量
        roots = []
        for p in Project.All:
            pyvim.Roots.append(p.root)
            root = DirNode(p.root, p.name)
            if not self.Title:
                info = p.info
                if not info:
                    self.Title = root.name
                else:
                    self.Title = "%s(%s)" % (root.name, info["branch"])

            roots.append(root)
        return roots

    def LS_Refresh_Hook(self):
        if self.first_fresh:
            self.first_fresh = False
            Project.emit("FrainEntry")
            return

    def LS_WinOpen_Hook(self):
        def vimleave():
            Project.emit("FrainLeave")

        pyvim.addevent('BufWritePost', libpath.push)
        pyvim.addevent('VimLeave',  vimleave)

class FrainList(FrainListSub):
    data = []
    def find(self):
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
            return 'NROOT' # not found root

        names = utils.getnames(p.root, path)
        if LIST.LS_Find(self, names):
            return True

    def add(self, path, name = ''):
        "增加一个新的 project, 提供参数 path, name"
        path = libpath.realpath(path)
        if path:
            Project(path, name)

    def add_cur_path(self):
        path = utils.bufferpath()
        self.add(path, '')

    def cur_project(self):
        "返回当前 bufferf 所有在 project 对象"
        path = utils.bufferpath()
        for p in Project.All:
            if path.startswith(p.root):
                return p

class DirNode(Node):
    def __init__(self, path, name = ''):
        if not name:
            name = libpath.basename(path)
        Node.__init__(self, name)
        self.path = path
        self.subnodes = False

    def LS_Node_Init(self): #初始子节点的方法
        if self.subnodes:
            return True

        dirs, names = libpath.listdir(self.path)
        if dirs == None:
            return

        names = black_filter_files(names)
        names = sorted_by_expand_name(names)

        dirs  = sorted(black_filter_files(dirs))

        self.subnodes = True

        for n in names:
            p = libpath.join(self.path, n)
            self.append(FileNode(p))

        for d in dirs:
            p = libpath.join(self.path, d)
            self.append(DirNode(p))
        return True

class FileNode(Leaf):
    def __init__(self, path):
        Leaf.__init__(self, libpath.basename(path))
        self.path = path

    def LS_Leaf_Edit(self):
        vim.command( "update")
        path = libpath.pull(self.path)
        if not path:
            return
        vim.command( "e %s" % path )


if __name__ == "__main__":
    pass

