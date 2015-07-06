#encoding:utf8
import os
import sys
from pyvim import log as logging

import vim
import pyvim
from imutils import emit_event, Redirect
import imrc
from plugins import Plugins
import ext
import handle_base
import handle_prompt

import string
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
        logging.info("load handle: %s : %s", name, handle)

def IM_Init():
    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    ftpath = os.path.join(ftpath, 'handles')

    load_handles('base', handle_base)
    load_handles('prompt', handle_prompt)

    plugins = Plugins(ftpath)
    plugins.hook_init = load_handles
    plugins.loads()

    Redirect().log()


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
                            (key, name, cls)
            #logging.debug(command)
            vim.command(command)

def call(handle, key, tp):
    """
       调用 handle, 依赖于 tp 调用不同的接口
    """
    attr_nm = "im_%s" % tp
    if not hasattr(handle, attr_nm):
        return

    return getattr(handle, attr_nm)(key)

def redirect(key, tp):
    """
       重定向处理
    """
    ft = vim.eval('&ft')
    syn = pyvim.syntax_area()

    handle_list = Redirect().get(ft, syn)
    for hd in handle_list:
        handle = __Handles.get(hd)
        if not handle:
            logging.error('not found handle: %s' % hd)
            continue
        logging.error('redirct to handle: %s:%s', hd, handle)
        if call(handle, key, tp):
            break

def IM(event, tp='key'):
    """
       处理事件.
       @tp: 表示当前的收到的事件的类型
       @event: 收到的事件

       tp 可以是 digit, upper, lower, punc, mult 也可以是 event
    """
    env.init()

    emit_event('start')

    if pyvim.pumvisible():
        logging.error('pumvisible');
        if not call('prompt', event, tp):
            redirect(event, tp)
    else:
         redirect(event, tp)

    emit_event('pre-stop')

    emit_event('stop')

if __name__ != "__main__":
    IM_Init()
