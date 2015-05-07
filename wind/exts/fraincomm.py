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

@pyvim.cmd(pyvim.complete.file)
def Frain(path='.', name=''):
    global frain
    if not frain:
        frain = LIST()
    frain.data.append((path,name))
    frain.refresh()

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
