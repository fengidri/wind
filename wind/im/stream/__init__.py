# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-26 11:43:25
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import im.imrc as imrc
import pyvim
import vim
from pyvim import log
import string
import frainui
import im.env as env
import im.prompt as prompt


__map = {}

def genmap(s):
    for ft in s.fts:
        __map[ft] = s


def Init():
    keys = {
            'digit': string.digits,
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'punc': string.punctuation,
            'mult': ['<tab>', '<bs>', '<cr>', '<space>', '<esc>', '<c-j>']
            }

    for cls, v in keys.items():
        for k in v:
            key = k
            name = k
            if k == '|': name = key = '\\|'
            if k == '\\': name = '\\\\'

            if key == '"' : name = '\\%s' % key

            if cls == 'mult':
                name = name.replace('<', '<lt>')

            command='inoremap <expr> %s Input_Monitor("%s", "%s")' % \
                            (key, cls, name)
            vim.command(command)


import im.handler as handler

from . import code
from . import tex

genmap(code.IM_Code())
genmap(tex.IM_Tex())


def handle(tp, key):
    tp = "im_%s" % tp
    log.debug("stream handle ft: %s syn: %s", env.ft, env.syntax)

    if env.ft.startswith('frainui'):
        frainui.inputstream(tp, key)
        return

    if env.pumvisible:
        if prompt.stream(tp, key):
            return

        handler.HD_Prompt.handler(tp, key)
        return

    __map.get(env.ft, handler.HD_WubiStream).handler(tp, key)


