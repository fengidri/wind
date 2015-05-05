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
    for path, name in frainpaths:
        frain.data.append((path,name))
    frain.refresh()



#############################
# path exp
#############################
class FrainStart( pyvim.command ):
    def add_path_from_param(self):
        if len(self.params) > 0:#处理path, name 两个参数
            path = self.params[0]
        else:
            path = '.'

        name = ''
        if len(self.params) > 1:
            name = self.params[1]

        frain.data.append((path,name))


    def run( self ):
        global frain
        if not frain:
            frain = LIST()
        #------------------------

        self.add_path_from_param()
        frain.refresh()

    def setting(self):
        self.set_complete(self.complete_file)#设置命令补全为文件

class FrainAdd(FrainStart):
    def run(self):
        self.add_path_from_param()
        frain.refresh()

class FrainSUBCommand(pyvim.command):
    def run(self):
        if frain:
            self._run()
        else:
            return


class FrainOpen(FrainSUBCommand):
    def _run(self):
        frain.open()

class FrainClose(FrainSUBCommand):
    def _run(self):
        frain.close()

class FrainFind(FrainSUBCommand):
    def _run( self ):
        s = frain.find()
        if s == 'NROOT':
            frain.add_cur_path()
            frain.refresh()
            frain.find()






class FrainFocus(FrainSUBCommand):
    def _run(self):
        frain.focus()

class FrainRefresh(FrainSUBCommand):
    def _run( self ):
        frain.refresh()
        return
        #刷新path exp 窗口之后. 展开显示当前正在编辑的文件
        for w in vim.windows:
            b = w.buffer
            if b.options['buftype'] != '':
                continue

class Project( pyvim.command ):
    def run( self ):
        from frain_libs import frnames, fropen
        from vuirpc import VuiClient
        def popen(response):
            cfg, rt = fropen(response.msg)

            global frain
            frain = LIST()
            for p in cfg.src_path:
                frain.data.append((p.path, p.name))
            frain.refresh()

        client = VuiClient()
        client.sethandle(200, popen)
        client.request("/open/project", {"values":frnames()})
        client.response()



class ProjectTerminal(pyvim.command):
    def run(self):
        if not frain:
            os.system('setsid xterm&')
            return

        path = frain.cur_root_path()
        if path:
            os.system('cd %s;setsid xterm&' % path)
        else:
            os.system('setsid xterm&')










