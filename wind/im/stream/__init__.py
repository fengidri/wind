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



from . import code
from . import tex
from . import wubi

code_gen = code.IM_Code()
code_lua = code.IM_Lua()

tex = tex.IM_Tex()
wubi = wubi.IM_Wubi()



def handle(tp, key):
    tp = "im_%s" % tp
    log.debug("stream handle ft: %s syn: %s before: %s", env.ft, env.syntax,
            env.before)

    if env.ft.startswith('frainui'):
        frainui.inputstream(tp, key)
        return

    if env.pumvisible:
        prompt.stream(tp, key)
        return

    if env.ft in tex.fts:
        tex.handler(tp, key)

    elif 'lua' == env.ft:
        code_lua.handler(tp, key)

    elif env.ft in code_gen.fts:
        code_gen.handler(tp, key)

    else:
        wubi.handler(tp, key)


