#encoding:utf8
import os
import sys
import logging

import vim
import pyvim
from imutils import key_all, key_feed, emit_event
import imrc
from plugins import Plugins
import ext

import string

ftmode = {} # 记录每一种文件类型对应的处理类

def load_ftmode(m):
    if not hasattr(m, 'im_ft'):
        return

    f = m.im_ft()

    for ft in f.im_ft:
        ftmode[ft] = f

def IM_Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'filetype')

    plugins = Plugins(ftpath)
    plugins.hook_init = load_ftmode
    plugins.loads()

    for ft, cls in ftmode.items():
        logging.error('%s: %s' % (ft, cls))

    keys = {
            'digit': string.digits,
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'punc': string.punctuation,
            'mult': ['<tab>', '<bs>', '<cr>', '<space>', '<esc>', '<c-j>']
            }

    for cls, v in keys.items():
        for k in v:
            if cls == 'mult' or v == '"': pre = '\\'
            else: pre = ''

            command='inoremap <expr> %s Input_Monitor("%s%s", "%s")' % 
                            (k, pre, k, cls)
            vim.command(command)


def IM(event, tp='key'):
    emit_event('start')

    emit_event('ft_pre')
    ft = vim.eval('&ft')
    im = ftmode.get(ft, None)# 按照文件类型得到对应的filetype 处理方法

    if im == None:
        if tp == 'key':
            key_feed(event)
    else:
        im.im(event, tp)

    emit_event('ft_post')

    emit_event('stop')

if __name__ != "__main__":
    IM_Init()
