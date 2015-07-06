#encoding:utf8
import os
import sys
import string
from pyvim import log as logging

import vim
import pyvim

from imutils import emit_event, Redirect
from plugins import Plugins
import handle_base
import handle_prompt
import prompt

import imrc
import ext
import env

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

def IM_Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'handles')

    load_handles('base', handle_base)
    load_handles('prompt', handle_prompt)

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

    logging.error('redirct to handle: %s', hd)

    return getattr(handle, attr_nm)(key)

def redirect(tp, key):
    """
       重定向处理
    """
    if pyvim.pumvisible():
        if call("prompt", tp, key):
            return

    ft = vim.eval('&ft')
    syn = pyvim.syntax_area()

    handle_list = Redirect().get(ft, syn)
    for hd in handle_list:
        if call(hd, tp, key):
            break

    call("activeprompt", tp, key)

import wubi


prompt.init(wubi.handle1, wubi.wubi)

def IM(*args):
    """
       处理事件.
       @tp: 表示当前的收到的事件的类型
       @event: 收到的事件

       tp 可以是 digit, upper, lower, punc, mult 也可以是 event
    """

    cls = args[0]
    env.init()
    logging.error(args)

    emit_event('start')
    if cls == "prompt":
        prompt.handle(*args[1:])

    elif cls == "key":
         redirect(*args[1:])

    elif cls == "event":
        redirect(*args)

    emit_event('pre-stop')

    emit_event('stop')
    #elif pyvim.pumvisible():
    #    if not call('prompt', event, tp):
    #        redirect(event, tp)

if __name__ != "__main__":
    IM_Init()
