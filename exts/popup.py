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
    p = popup.PopupSystem('ping www.baidu.com')


@pyvim.cmd()
def PopupMenu():
    menu = ['MailSend', 'MailNew', "Mail Mark Read"]

    def finish(i):
        print(menu[i])

    popup.PopupMenu(menu, finish)

