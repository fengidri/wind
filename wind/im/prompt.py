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

class g:
    active = None

class Prompt(object):
    _prompt = []
    co_done = 0

    def __init__(self, key_handler = None):
        self.keyhandler = key_handler

    def active(self):
        func = "wind#Prompt"

        vim.command("let &omnifunc='%s'" % func)
        vim.command("let &l:omnifunc='%s'" % func)

        imrc.feedkeys('\<C-X>\<C-O>')

        g.active = self

    def co_active(self):
        self.co_done += 1
        self.active()

    def append_string(self, ppt):
        self._prompt.append({"word": ppt})

    def append_list(self, ppt):
        for x in ppt:
            if isinstance(x, dict):
                self._prompt.append(x)

            elif isinstance(x, basestring):
                self.append_string(x)



    def append(self, ppt):
        if isinstance(ppt, list):
            self.append_list(ppt)

        elif isinstance(ppt, basestring):
            self.append_string(ppt)

    def build(self, word, abbr = None, menu = None):
        s = {"word": word}
        if abbr:
            s["abbr"] = abbr

        if menu:
            s["menu"] = menu

        return s

    def abuild(self, word, abbr = None, menu = None):
        self._prompt.append(self.build(word, abbr, menu))


    def popmenu(self):
        if not self._prompt:
            return

        vim.vars["omniresult"] = self._prompt
        vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1

    def findstart(self):
        pass

    def base(self, b):
        pass

def Findstart(col):
    if not isinstance(col, int):
        col = -3

    if col > -1:
        _col = env.col - col
        return _col
    return col


def handle(event, base=None):
    if event == 'done':
        if g.active.co_done:
            g.active.co_done -= 1
            return

        g.active = None
        return

    if event == "findstart":
        vim.vars["omnicol"] = Findstart(g.active.findstart())
        return

    if event == "base":
        g.active.base(base)

        words = g.active._prompt

        vim.vars["omniresult"] = {'words':words, 'refresh': 'always'}

        del g.active._prompt[:]


def stream(tp, key):
    if g.active and g.active.keyhandler:
        g.active.keyhandler.handler(tp, key)
        return True














