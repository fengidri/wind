# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 10:57:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import imrc
import logging
import vim
from im.imrc import feedkeys
from pyvim import  pumvisible
import os

__event_cb = {}

def emit_event(event):
    cblist = __event_cb.get(event)
    if not cblist:
        return
    for cb in cblist:
        cb()

def add_hook(event, cb):
    cblist = __event_cb.get(event)
    if not cblist:
        __event_cb[event] = [cb]
    else:
        cblist.append(cb)


class Redirect(object):
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(Redirect, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'ft'):
            return

        self.ft = {}
        path = os.path.realpath(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, 'redirect.conf')
        if not os.path.exists(path):
            return
        self.load_reds(path)

    def load_reds(self, path):
        "load redirects"

        tmp = []
        lines = open(path).readlines()
        for line in lines:
            if line[0] == '>':
                self.handle_block(tmp)
                del tmp[:]
                tmp.append(line[1:])
            tmp.append(line)
        self.handle_block(tmp)


    def handle_block(self, lines):
        if not lines: return

        fts = [ft.strip() for ft in lines[0].split(',')]

        syntax = {}
        for line in lines[1:]:
            tt = line.split(':')
            if len(tt) != 2:
                continue
            syn = [t.strip() for t in tt[0].split(',')]
            handle_list = [t.strip() for t in tt[1].split(',')]
            for s in syn:
                syntax[s] = handle_list

        for f in fts:
            self.ft[f] = syntax


    def get(self, ft, syntax):
        reds = self.ft.get(ft)
        if not reds:
            ft = '*'

        reds = self.ft.get(ft)
        if not reds:
            return ["base"]

        handle_list = reds.get(syntax)
        if not handle_list:
            syntax = '*'

        handle_list = reds.get(syntax)
        if not handle_list:
            return ["base"]

        return handle_list

    def log(self):
        for ft, v in self.ft.items():
            logging.info("Redirects: %s: %s", ft, v)


def key_to_feed(key):
    if key in imrc.digits:
        return key

    elif key in imrc.lowerletter:
        return key

    elif key in imrc.upperletter:
        return key

    elif key in imrc.puncs:
        return imrc.puncs.get(key)[1]

    elif key in imrc.mults:
        return imrc.mults.get(key)[1]
    else:
        logging.error("key:%s is not imrc" % key)

def key_to_see(key):
    if key in imrc.digits:
        return key
    elif key in imrc.lowerletter:
        return key
    elif key in imrc.upperletter:
        return key
    elif key in imrc.puncs:
        return imrc.puncs.get(key)[0]
    elif key in imrc.mults:
        return imrc.mults.get(key)[0]



class SelMenu( object ):
    "基于omnicomplete 包装成的SelMenu"
    "默认使用内部的complete function"
    "也可以指定omnicomplete function "

    omnifunc = "vimlib#SelMenuFunction"
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(SelMenu, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def check_omnifunc( self, func ):
        if vim.eval( '&l:omnifunc' ) != func:
            vim.command("let &omnifunc='%s'" % func)
            vim.command("let &l:omnifunc='%s'" % func)

    def showlist(self, words_list, length):
        """ 与show 比较相似, 只是使用 输入的是list, 也就说是比较简单的结构"""
        words = []
        for w in words_list:
            words.append({"word": w})
        self.show(words, length)

    def show( self, words, length ):
        """使用内部的补全函数进行输出
                @words:   vim 格式的数据结构
                @length:  光标前要进行补全的字符长度
        """
        self.words = words
        vim.vars["omniresult"] = words
        vim.vars["omnicol"] = vim.current.window.cursor[1] - length + 1
        self.complete(self.omnifunc)


    def complete(self, fun):
        "指定补全函数"
        logging.error('#-------------')
        self.check_omnifunc(fun)
        feedkeys('\<C-X>\<C-O>\<C-P>')

    def select(self, nu):
        if pumvisible( ):
            feedkeys((nu + 1) * '\<C-N>')
            feedkeys( '\<C-Y>')

    def getselect(self, nu):
        if pumvisible( ):
            feedkeys( '\<C-Y>' )
        return self.words[nu]

    def cencel( self ):
        feedkeys('\<C-e>')




if __name__ == "__main__":
    pass

