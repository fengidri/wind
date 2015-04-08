#encoding:utf8
import pyvim
import vim

from frain_libs import paths_exp
from frain_libs import data


from frain_libs import project

from vuirpc import VuiClient

from frain_libs import fropen
from frain_libs import frnames
from frain_libs import mescin

import os


#############################
# path exp
#############################
class PathsExp( pyvim.command ):
    def run( self ):
        global listwin
        listwin = LIST()
        listwin.append(DirNode('/home/feng/nginx'))
        listwin.append(DirNode('/tmp'))
        listwin.refresh()
        return
        if len(self.params) > 0:#处理path, name 两个参数
            path = self.params[0]
            try:
                name = self.params[1]
            except:
                name = ""
            if not path.startswith('/'):
                p = os.path.dirname(vim.current.buffer.name) or os.getcwd()
                path = os.path.join(p, path)
                path = os.path.realpath(path)

            data.append_path(path, name)

        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )
    def setting( self ):
        self.set_complete( self.complete_file )#设置命令补全为文件

class PathsExpFilter( pyvim.command ):
    def run( self ):
        paths_exp.blacklist_switch = not paths_exp.blacklist_switch
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )

class PathsExpRefresh( pyvim.command ):
    def run( self ):
        paths_exp.refresh_nodes( )
        paths_exp.refresh_win( )
        #刷新path exp 窗口之后. 展开显示当前正在编辑的文件
        for w in vim.windows:
            b = w.buffer
            if b.options['buftype'] != '':
                continue
            paths_exp.open_to_file( b.name )

class PathsExpOpen( pyvim.command ):
    def run( self ):
        listwin.open()

        #paths_exp.paths_exp_open( )

class PathsExpFind( pyvim.command ):
    def run( self ):
        path = pyvim.vim.current.buffer.name
        if not path:
            return
        if pyvim.vim.current.buffer.options['buftype'] != '':
            return
        if paths_exp.goto_path_exp_win( ):
            paths_exp.open_to_file( path )

class PathsExpGo(pyvim.command):
    def run(self):
        paths_exp.goto_path_exp_win( )



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







from frainui import LIST
from frainui import Node, Leaf
import libpath
import logging

class DirNode(Node):
    def __init__(self, path):
        Node.__init__(self, libpath.basename(path))
        self.path = path

    def OpenPre(self):
        if self.sub_nodes:
            return True
        dirs, names = libpath.listdir(self.path)
        names = sorted(names)
        dirs  = sorted(dirs)
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

    def open(self):
        vim.command( "update")
        vim.command( "e %s" % self.path )








