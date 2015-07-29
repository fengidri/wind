# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 10:57:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
from pyvim import log
import vim
import os
import env

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
            if len(tt) != 3:
                continue
            syn = [t.strip() for t in tt[0].split(',')]
            stream_handle_list = [t.strip() for t in tt[1].split(',')]
            prompt_handle_list = [t.strip() for t in tt[2].split(',')]
            for s in syn:
                syntax[s] = (stream_handle_list,  prompt_handle_list)

        for f in fts:
            self.ft[f] = syntax

    def getcur(self, cls):
        return self.get(cls, env.ft, env.syntax)


    def get(self, cls, ft, syntax):
        default = ['base']
        if cls == 'prompt':
            default = []
        reds = self.ft.get(ft)
        if not reds:
            ft = '*'

        reds = self.ft.get(ft)
        if not reds:
            return default

        handle_list = reds.get(syntax)
        if not handle_list:
            syntax = '*'

        handle_list = reds.get(syntax)
        if not handle_list:
            return default

        if cls == 'prompt':
            return handle_list[1]
        else:
            return handle_list[0]

    def log(self):
        for ft, v in self.ft.items():
            log.info("Redirects: %s: %s", ft, v)






if __name__ == "__main__":
    pass

