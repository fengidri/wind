# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
import vim
frain = None
frainpaths   = [('/tmp', 'tmpdir')]

def frainopen():
    global frain
    frain = LIST()
    for path, name in frainpaths:
        frain.append(DirNode(path, name))
    frain.refresh()



#############################
# path exp
#############################
class FrainStart( pyvim.command ):
    def run( self ):
        if len(self.params) > 0:#处理path, name 两个参数
            path = self.params[0]
        else:
            return

        path = libpath.realpath(path)

        name = ''
        if len(self.params) > 1:
            name = self.params[1]

        frainpaths.append((path, name))
        frainopen()

    def setting(self):
        self.set_complete(self.complete_file)#设置命令补全为文件

class FrainOpen( pyvim.command ):
    def run(self):
        if frain:
            frain.open()

class FrainFind(pyvim.command):
    def run( self ):
        if not frain:
            return

        path = libpath.bufferpath()
        logging.error('-----------%s', path)
        names = libpath.getnames('/home/feng/nginx', path)
        frain.find(names)

class FrainFocus(pyvim.command):
    def run(self):
        if not frain:
            return
        frain.focus()

class FrainRefresh( pyvim.command ):
    def run( self ):
        if not frain:
            return
        frain.refresh()
        return
        #刷新path exp 窗口之后. 展开显示当前正在编辑的文件
        for w in vim.windows:
            b = w.buffer
            if b.options['buftype'] != '':
                continue


class PathsExpFilter( pyvim.command ):
    def run( self ):
        paths_exp.blacklist_switch = not paths_exp.blacklist_switch
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )





class Project( pyvim.command ):
    def run( self ):
        def popen(response):
            fropen(response.msg)
        client = VuiClient()
        client.sethandle(200, popen)
        client.request("/open/project", {"values":frnames()})
        client.response()

class ProjectSync(pyvim.command):
    def run( self ):
        if not project.Project:
            return
        project.Project.sync()
"""
    -- 无视时间, 同步所有的文件
"""
class ProjectSyncAll( pyvim.command ):
    def run( self ):
        if not project.Project:
            return
        project.Project.sync( syncall=True )



class ProjectTerminal(pyvim.command):
    def run(self):
        rs = data.get_path()
        cur = vim.current.buffer.name
        for r in rs:
            if cur.startswith(r):
                os.system('cd %s;setsid xterm&' % r)
                break
        else:
            os.system('setsid xterm&')


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





from frainui import LIST
from frainui import Node, Leaf
import libpath
import logging
import re

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
        vim.command( "e %s" % self.path )








