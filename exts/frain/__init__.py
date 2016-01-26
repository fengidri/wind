# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:56:54
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import pyvim
import os

import project
import frain
import libpath

FrainList = None

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    global FrainList
    if not FrainList:
        FrainList = frain.FrainList()

    path = libpath.realpath(path)
    if not path:
        return
    if not name:
        name = libpath.basename(path)

    if path:#TODO maybe scp
        project.Project(path, name)

    FrainList.listwin.refresh()

    # add cmd
    pyvim.cmd(pyvim.complete.file)(FrainToggle)
    pyvim.cmd(pyvim.complete.file)(FrainAddInclude)

def FrainToggle(path='.', name=''):
    FrainList.listwin.BFToggle()


def FrainAddInclude(path):
    path = os.path.realpath(path)
    project.CInc(path)

    project.Project.update_c_include()


if __name__ == "__main__":
    pass

