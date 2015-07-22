# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim

import vim
from frain import FrainList
from kvcache import KvCache
from project import Project

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    FrainList().add(path, name)


@pyvim.cmd()
def ProjectTerminal():
    if not FrainList.get_instance():
        os.system('setsid xterm&')
        return
    p = FrainList().cur_project()
    if p:
        os.system('cd %s;setsid xterm&' % p.root)
    else:
        os.system('setsid xterm&')

@pyvim.cmd(pyvim.complete.file)
def FrainAddInclude(path):
    if not FrainList.get_instance():
        return

    project = FrainList().cur_project()
    if not project:
        return

    if not os.path.isdir(path):
        pyvim.echoline('%s is not dir' % path)
        return

    path = os.path.realpath(path)

    project.add_c_include(path)
    Project.update_c_include()




