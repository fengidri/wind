# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-07 09:13:23
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import string
import os
from imutils import Redirect
from plugins import Plugins

import imrc
import pyvim
import vim
from pyvim import log
import env

import frainui

__Handles = {}

def stream(name): # use for stream plugin
    def _fun(cls):
        register(name, cls())
        return cls
    return _fun

def register(name, obj): # api
    __Handles[name.lower()] = obj

def Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'stream')

    plugins = Plugins(ftpath)
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
            if k == '|': name = key = '\\|'
            if k == '\\': name = '\\\\'

            if key == '"' : name = '\\%s' % key

            if cls == 'mult':
                name = name.replace('<', '<lt>')

            command='inoremap <expr> %s Input_Monitor("%s", "%s")' % \
                            (key, cls, name)
            vim.command(command)


def call(handles, tp, key):
    for handle in handles:
        attr_nm = "im_%s" % tp
        getattr(handle, attr_nm)(key)

def handle(tp, key):
    """
       重定向处理
    """
    if env.ft.startswith('frainui'):
        frainui.inputstream(tp, key)
        return

    if pyvim.pumvisible():
        if getattr(__Handles.get("prompt"), 'im_%s' % tp)(key):
            return

    name_list = Redirect().getcur('stream')
    handle_list = []
    for n in name_list:
        h = __Handles.get(n)
        if h:
            handle_list.append(h)

    call(handle_list, tp, key)
    getattr(__Handles.get("activeprompt"), 'im_%s' % tp)(key)
 #   call(__Handles"activeprompt", tp, key)

if __name__ == "__main__":
    pass

