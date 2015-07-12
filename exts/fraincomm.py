# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim

import vim
from frain import LIST
from kvcache import KvCache
from project import Project

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    frain = LIST()
    frain.add(path, name)
    frain.refresh()


@pyvim.cmd()
def FrainOpen():
    if not LIST.get_instance():
        return
    LIST().open()

@pyvim.cmd()
def FrainClose():
    if not LIST.get_instance():
        return
    LIST().close()

@pyvim.cmd()
def FrainFind():
    if not LIST.get_instance():
        return
    frain = LIST()
    s = frain.find()
    if s == 'NROOT':
        frain.add_cur_path()
        frain.refresh()
        frain.find()

    if not s:
        frain.refresh()
        frain.find()

@pyvim.cmd()
def FrainFocus():
    if LIST.get_instance():
        LIST().focus()

@pyvim.cmd()
def FrainRefresh():
    if LIST.get_instance():
        LIST().refresh()
    #刷新path exp 窗口之后. 展开显示当前正在编辑的文件

@pyvim.cmd()
def ProjectTerminal():
    if not LIST.get_instance():
        os.system('setsid xterm&')
        return
    p = LIST().cur_project()
    if p:
        os.system('cd %s;setsid xterm&' % p.root)
    else:
        os.system('setsid xterm&')


@pyvim.cmd()
def ProjectX():
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

@pyvim.cmd(pyvim.complete.file)
def FrainAddInclude(path):
    if not LIST.get_instance():
        return

    project = LIST().cur_project()
    if not project:
        return

    if not os.path.isdir(path):
        pyvim.echoline('%s is not dir' % path)
        return

    path = os.path.realpath(path)

    project.add_c_include(path)
    Project.update_c_include()




