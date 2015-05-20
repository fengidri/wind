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

class Session(object):
    DBFile = os.path.join(os.environ.get("HOME"), '.cache/frain/session')
    def __init__(self):
        dbdir = os.path.dirname(self.DBFile)
        if not os.path.exists(dbdir):
            os.mkdir(dbdir)

    def _load(self):
        if not os.path.exists(self.DBFile):
            return {}
        else:
            c = open(self.DBFile).read()
            return json.loads(c)
    def get(self, path):
        return self._load().get(path)

    def _save(self, se):
        c = json.dumps(se)
        open(self.DBFile, 'w').write(c)

    def save(self):
        session = self._load()
        cur_session = self.getcurfile()
        session.update(cur_session)
        self._save(session)

    def getcurfile(self):
        fs = {}
        for w in vim.windows:
            name = w.buffer.name
            if not name:
                continue
            for path in pyvim.Roots:
                if name.startswith(path):
                    l = fs.get(path)
                    if l == None:
                        fs[path] = [name]
                    else:
                        l.append(name)
                    break

        return fs



############################ FrainList #########################################
class FrainList(LIST):
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
        if LIST.find(self, names):
            return True

    def add_cur_path(self):
        path = utils.bufferpath()
        self.data.append((libpath.dirname(path), ''))

    def addlist(self):
        pyvim.Roots = []  # 整个vim 可用的变量
        data = []
        for path, name in self.data:
            path = libpath.realpath(path)
            if path in pyvim.Roots:
                continue
            pyvim.Roots.append(path)
            data.append((path, name))
            LIST.append(self, DirNode(path, name))
        self.data = data

    def OpenLastFiles(self):
        pyvim.origin_win()
        files = Session().get(pyvim.Roots[0])
        if files:
            pyvim.openfiles(files)

    def OnWinPost(self):
        pyvim.addevent('BufWritePost', libpath.push)
        pyvim.addevent('VimLeave',  Session().save)

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

    def InitSub(self): #初始子节点的方法
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

    def edit(self):
        vim.command( "update")
        path = libpath.pull(self.path)
        if not path:
            return
        vim.command( "e %s" % path )


if __name__ == "__main__":
    pass

