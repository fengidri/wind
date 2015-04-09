# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
import vim
from frain import LIST
frain = None
frainpaths   = []

def frainopen():
    global frain
    frain = LIST()
    for path, name in frainpaths:
        frain.append(path, name)
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
        frain.find()

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
        from frain_libs import frnames, fropen
        from vuirpc import VuiClient
        def popen(response):
            cfg, rt = fropen(response.msg)

            global frain
            frain = LIST()
            for p in cfg.src_path:
                frain.append(p.path, p.name)
            frain.refresh()

        client = VuiClient()
        client.sethandle(200, popen)
        client.request("/open/project", {"values":frnames()})
        client.response()



class ProjectTerminal(pyvim.command):
    def run(self):
        if not frain:
            return

        path = frain.cur_root_path()
        if path:
            os.system('cd %s;setsid xterm&' % path)
        else:
            os.system('setsid xterm&')










