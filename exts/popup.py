# -*- coding:utf-8 -*-

import vim
import pyvim
import popup



def filter_cb(ws, bw):
    o = []
    lines = open('/home/xuanzhuo.dxf/nvme/kernel/upstream-stable/net/ipv4/tcp.c').readlines()
    for line in lines:
        for w in ws:
            if line.find(w) == -1:
                break
        else:
            o.append(line)

    return o



def finish_cb(line_nu):
    vim.current.buffer[0] = str(line_nu)

@pyvim.cmd()
def Popup():
    p = popup.PopupSearch(filter_cb, finish_cb)


