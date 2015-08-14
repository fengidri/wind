# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:56:54
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


from frain import FrainList
import pyvim

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    FrainList().add(path, name)

@pyvim.cmd(pyvim.complete.file)
def FrainToggle(path='.', name=''):
    FrainList().listwin.BFToggle()


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


if __name__ == "__main__":
    pass

