# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 17:44:43
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim

import vim
from frain import LIST, set_cinclude
from kvcache import KvCache
frain = None

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    global frain
    flag = False
    if not frain:
        frain = LIST()
        flag = True
    frain.data.append((path,name))
    frain.refresh()
    if flag:
        frain.OpenLastFiles()


@pyvim.cmd()
def FrainOpen():
    if not frain:
        return
    frain.open()

@pyvim.cmd()
def FrainClose():
    if not frain:
        return
    frain.close()

@pyvim.cmd()
def FrainFind():
    if not frain:
        return
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
    if not frain:
        return
    frain.focus()

@pyvim.cmd()
def FrainRefresh():
    if not frain:
        return
    frain.refresh()
    return
    #刷新path exp 窗口之后. 展开显示当前正在编辑的文件
    for w in vim.windows:
        b = w.buffer
        if b.options['buftype'] != '':
            continue

@pyvim.cmd()
def ProjectTerminal():
    if not frain:
        os.system('setsid xterm&')
        return

    path = frain.cur_root_path()
    if path:
        os.system('cd %s;setsid xterm&' % path)
    else:
        os.system('setsid xterm&')


@pyvim.cmd()
def Project():
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
    if not frain:
        return

    if not os.path.isdir(path):
        pyvim.echoline('%s is not dir' % path)

    kv = KvCache()
    path = os.path.realpath(path)

    root = frain.cur_root_path()
    incs = kv.get(root, ns="cinclude")
    if incs == None:
        incs = []

    if path in incs:
        return

    incs.append(path)
    kv.set(root, incs, ns='cinclude')
    kv.save()

    set_cinclude()

