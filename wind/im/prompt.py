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
import im.keybase

class PromptKey(im.keybase.BaseEnd):
    def cb_tab(self):
        imrc.feedkeys('\<C-n>')
        return True


    def cb_esc(self):
        imrc.feedkeys('\<esc>')
        return True

    def cb_enter(self):
        imrc.feedkeys('\<C-e>')
        return True

    def cb_space(self):
        #uchar = env.before[-1]
        #if (uchar >= u'u0041' and uchar<=u'u005a') or \
        #        (uchar >= u'u0061' and uchar<=u'u007a'):
        imrc.feedkeys('\<C-N>')
        imrc.feedkeys('\<C-Y>')
        return True

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


        if g.active == self:
            self.co_done += 1
        else:
            g.active = self

    def append_string(self, ppt):
        self._prompt.append({"word": ppt})

    def append_list(self, ppt):
        for x in ppt:
            if isinstance(x, dict):
                self._prompt.append(x)

            elif isinstance(x, str):
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
    log.debug("prompt findstart recv: %s" % col)
    if not isinstance(col, int):
        # vim help: complete-functions: To cancel silently and leave completion mode.
        col = -3

    if col > -1:
        _col = env.col - col
        return _col
    return col

from . import tips

def handle(event, base=None):
    log.debug("prompt: %s before: %s", g.active, env.before)
    if not g.active:
        return

    if event == 'done':
        if g.active.co_done:
            g.active.co_done -= 1
            return

        tips.do_tips()
        g.active = None
        return

    if event == "findstart":
        start = Findstart(g.active.findstart())
        log.debug("prompt findstart start: %s" % start)
        vim.vars["omnicol"] = start
        return

    if event == "base":
        g.active.base(base)

        words = g.active._prompt

        vim.vars["omniresult"] = {'words':words, 'refresh': 'always'}

        del g.active._prompt[:]



class g:
    active = None
    default_key = PromptKey()


def stream(tp, key):
    log.debug("prompt stream: %s %s" % (tp, key))
    if g.active and g.active.keyhandler:
        g.active.keyhandler.handler(tp, key)
        return True

    g.default_key.handler(tp, key)
















