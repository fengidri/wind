# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:44:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from frainui import LIST
from frainui import Node, Leaf
import libpath
import logging
import re
import vim
import pyvim
import utils
import os
import json
import gitinfo
from project import Project

blacklist_file=[
    "^\.",      "^tags$",
    ".+\.ac$", ".+\.pyc$" , ".+\.so$", ".+\.o$", ".+\.a$",
    ".+\.lo$"
    ]

blacklist_switch = True

def black_filter_files( files ):
    if not blacklist_switch:
        return True
    fs = []
    for f in files:
        for regex in blacklist_file:
            match = re.search( regex, f )
            if match:
                break
        else:
            fs.append(f)
    return fs



"""
    排序函数
"""
def sorted_by_expand_name( files ):
    files_type = { "c":[], "cpp":[], "h":[], "py":[], "other":[] }
    types = files_type.keys( )

    for f in files:
        try:
            type_name = f.split( '.' )[ -1 ]
        except:
            type_name = "other"
        if not type_name in types:
            type_name = "other"
        files_type[ type_name ].append( f )
    tmp = [  ]
    for v in files_type.values( ):
        tmp += v

    return sorted(files_type[ 'c' ]) +\
            sorted(files_type[ 'cpp' ]) +\
            sorted(files_type[ 'h' ]) +\
            sorted(files_type[ 'py' ]) +\
            sorted(files_type[ 'other' ])



############################ FrainList #########################################
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
        path = utils.bufferpath()
        if not path:
            return
        for root in self.root.sub_nodes:
            if path.startswith(root.path):
                break
        else:
            return 'NROOT' # not found root

        names = utils.getnames(root.path, path)
        if LIST.LS_Find(self, names):
            return True

    def add(self, path, name):
        path = libpath.realpath(path)
        Project(path, name)

    def add_cur_path(self):
        path = utils.bufferpath()
        self.data.append((libpath.dirname(path), ''))


    def cur_root_path(self):
        path = utils.bufferpath()
        for r in self.root.sub_nodes:
            if path.startswith(r.path):
                return r.path

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

