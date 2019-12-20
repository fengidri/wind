# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-05 13:01:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os

import vim
from pyvim import log
from . import imrc
from . import env

_prompt = []

################################################################################
def append_string(ppt):
    _prompt.append({"word": ppt})

def append_list(ppt):
    for x in ppt:
        if isinstance(x, dict):
            _prompt.append(x)

        elif isinstance(x, basestring):
            append_string(x)



def append(ppt):
    if isinstance(ppt, list):
        append_list(ppt)

    elif isinstance(ppt, basestring):
        append_string(ppt)

def build(word, abbr = None, menu = None):
    s = {"word": word}
    if abbr:
        s["abbr"] = abbr

    if menu:
        s["menu"] = menu

    return s

def abuild(word, abbr = None, menu = None):
    _prompt.append(build(word, abbr, menu))

################################################################################

def popmenu():
    if not _prompt:
        return
    vim.vars["omniresult"] = _prompt
    vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1

findstart = None
base = None

def Findstart():
    tt = None
    col = -3

    col = findstart()
    if not isinstance(col, int):
        col = -3

    if col > -1:
        _col = env.col - col
        return _col
    return col

def Base(b):
    del _prompt[:]
    base(b)
    return _prompt

def handle(event, base=None):
    if event == 'done':
        env.pumvisible_handler = None
        return

    if event == "findstart":
        start = Findstart()
        vim.vars["omnicol"] =  start

    elif event == "base":
        vim.vars["omniresult"] = {'words':Base(base), 'refresh': 'always'}

