# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:56:54
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import pyvim
import os

import project
import frain

FrainList = None

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    global FrainList
    if not FrainList:
        FrainList = frain.FrainList()

    FrainList.add(path, name)

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

