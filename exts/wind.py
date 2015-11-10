# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-10-30 02:38:16
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from pyvim import log
from pyvim import cmd
import vim
import logging
from pyvim import statusline

subcmd = {'im' : {}}
subcmd['im']['wubi'] = ['on', 'off']

@cmd(complete = subcmd)
def Wind(t, *k):
    if t == 'im':
        try:
            if k[0] == 'wubi':
                if k[1] == 'on':
                    vim.vars['wind_im_wubi'] = 1
                else:
                    vim.vars['wind_im_wubi'] = 0
        except:
            pass
