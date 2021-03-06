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
import pyvim

class PromptKey(im.keybase.BaseEnd):
    def cb_tab(self):
        imrc.feedkeys('\<C-n>')
        return True


    def cb_enter(self):
        imrc.feedkeys(('\<C-y>', 'm'))
        return True

    def cb_space(self):
        imrc.feedkeys(' ')
        return True

    def im_punc(self, k):
        cb = self.cbs.get(k)
        if cb:
            cb()
        else:
            imrc.feedkeys('\<C-Y>')
            imrc.feedkeys(k)
        return True


    def output(self, k):
        imrc.feedkeys('\<C-Y>')
        return False # continue

    def cb_esc(self):
        # 回到原始的状态, 并关闭 prompt
        #imrc.feedkeys(('\<C-e>', 'm'))
        # TODO 这里输入的 c-y 好像没有起到作用, 手动输入是可以的
        # 要增加 m 这里就可以了, 但是还是不能和 c-e 一起
        imrc.feedkeys('\<esc>')
        return True

    def cb_backspace(self):
        # 这里的逻辑要分三步
        # 1. 接受当前的 prompt 状态, 并关闭 prompt
        # 2. 删除字符
        # 3. 再次触发 prompt.

        imrc.feedkeys('\<C-Y>')
        imrc.feedkeys('\<bs>')
        g.active.active()
        return False



    im_digit = im_upper = im_lower = output

    def im_punc(self, k):
        return self.run_handle(k)

    def im_mult(self, k):
        return self.run_handle(k)

    def handler(self, tp, key):
        return getattr(self, tp)(key)


class Prompt(object):
    _prompt = []
    trigger_key = '\<C-X>\<C-O>'

    def __init__(self, key_handler = None):
        self.keyhandler = key_handler


    def active(self, delay=True):
        func = "wind#Prompt"

        vim.command("let &omnifunc='%s'" % func)
        vim.command("let &l:omnifunc='%s'" % func)

        g.active = self

        if delay:
            imrc.feedkeys(self.trigger_key)
        else:
            pyvim.feedkeys(self.trigger_key)




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


def handle(event, base=None):
    log.debug("prompt active: %s before: %s, line: %s", g.active, env.before,
            vim.current.line)

    if not g.active:
        return

    active = g.active

    if event == 'done':
        #del g.queue[0]
        return

    if event == "findstart":
        start = Findstart(active.findstart())
        log.debug("prompt findstart start: %s" % start)
        vim.vars["omnicol"] = start
        return

    if event == "base":
        active.base(base)

        words = active._prompt

        vim.vars["omniresult"] = {'words':words, 'refresh': 'none'}

        del active._prompt[:]

    base = None



class g:
    active = None
    default_key = PromptKey()


def stream(tp, key):
    if g.active:
        active = g.active

        if active.keyhandler:
            active.keyhandler.handler(tp, key)
            return True

    return g.default_key.handler(tp, key)
















