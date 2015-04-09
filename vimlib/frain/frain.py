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

blacklist_file=[
    "^\.",      "^tags$",
    ".+\.ac$", ".+\.pyc$" , ".+\.so$", ".+\.o$"
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



class FrainList(LIST):
    title = ''
    def find(self):
        path = libpath.bufferpath()
        for root in self.root.sub_nodes:
            names = libpath.getnames(root.path, path)
            if names:
                LIST.find(self, names)
                return

    def append(self, path, name):
        path = libpath.realpath(path)
        n = DirNode(path, name)
        LIST.append(self, n)

    def OnWinPost(self):
        if self.title:
            self.settitle(self.title)
        pyvim.addevent('BufWritePost', '*', libpath.push)



    def cur_root_path(self):
        path = libpath.bufferpath()
        for r in self.root.sub_nodes:
            if path.startswith(r.path):
                return r.path





class DirNode(Node):
    def __init__(self, path, name = ''):
        if not name:
            name = libpath.basename(path)
        Node.__init__(self, name)
        self.path = path

    def OpenPre(self): # 打开节点前
        if self.sub_nodes:# 这会使空目录不断刷新
            return True

        dirs, names = libpath.listdir(self.path)
        names = black_filter_files(names)
        dirs  = black_filter_files(dirs)
        names = sorted_by_expand_name(names)

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

    def edit(self):
        vim.command( "update")
        path = libpath.pull(self.path)
        if not path:
            return
        vim.command( "e %s" % path )


if __name__ == "__main__":
    pass

