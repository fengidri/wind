# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-07 09:13:23
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import string
import os
from imutils import emit_event, Redirect
from plugins import Plugins

import imrc
import pyvim
import vim
from pyvim import log

__Handles = {}

def load_handles(m_name, module):
    m_name = m_name.lower()
    t_attr = "im_%s" % m_name
    for attr in dir(module):
        if attr.lower() != t_attr:
            continue

        name = attr[3:].lower()
        handle = getattr(module, attr)()
        __Handles[name] = handle
        #logging.info("load handle: %s : %s", name, handle)

def Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'stream')

    #load_handles('base', handle_base)
    #load_handles('prompt', handle_prompt)

    plugins = Plugins(ftpath)
    plugins.hook_init = load_handles
    plugins.loads()

    Redirect()#.log()

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
            if k == '|': key = '\\%s' % k

            if key == '"' : name = '\\%s' % key

            if cls == 'mult':
                name = name.replace('<', '<lt>')

            command='inoremap <expr> %s Input_Monitor("%s", "%s")' % \
                            (key, cls, name)
            vim.command(command)

def call(hd, tp, key):
    """
       调用 handle, 依赖于 tp 调用不同的接口
    """

    handle = __Handles.get(hd)
    if not handle:
        return

    attr_nm = "im_%s" % tp
    if not hasattr(handle, attr_nm):
        return

    log.error('redirct to handle: %s', hd)

    return getattr(handle, attr_nm)(key)

def handle(tp, key):
    """
       重定向处理
    """
    if pyvim.pumvisible():
        if call("prompt", tp, key):
            return



    handle_list = Redirect().getcur('stream')
    for hd in handle_list:
        if call(hd, tp, key):
            break

    call("activeprompt", tp, key)

if __name__ == "__main__":
    pass

