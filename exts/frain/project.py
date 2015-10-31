# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-21 10:59:34
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import os
import json
import logging

import pyvim
import vim
import gitinfo
import utils

from kvcache import KvCache
VARS = ["wind_im_wubi"]

class Project(object):
    All = []
    @classmethod
    def emit(cls, single):
        func = 'Hook_%s' % single
        logging.error(func)

        if hasattr(cls, func):
            getattr(cls, func)()

    @classmethod
    def Hook_FrainEntry(cls):
        cls.update_c_include()

        update_vim_vars(cls.All[0].kvdb.get("vim_vars"))

        #switch edit space
        pyvim.origin_win()

        ## last open
        if len(cls.All) > 0:
           files = cls.All[0].kvdb.get("lastopen")
           logging.error(files)
           if files:
                 pyvim.openfiles(files)

    @classmethod
    def Hook_FrainLeave(cls):
        for p in cls.All:
            p.save_curfile()
            p.save_vars()
            p.kvdb.save()


    @classmethod
    def update_c_include(cls):
        cins = {}
        for p in cls.All:
            incs = p.kvdb.get("cinclude")
            if incs:
                cins[p.root] = incs

        if cins:
            vim.vars['frain_include_dirs'] = json.dumps(cins)
            # try cache Ycm's flag cache
            #vim.command('silent YcmCompleter ClearCompilationFlagCache')


    def __init__(self, root, name = ''):
        self.root = root
        self.name = name

        self.kvdb = KvCache(os.path.join(self.root, '.wind'))

        self.gitinfo = gitinfo.gitinfo(root)
        Project.All.append(self)

    def close(self):
        self.save_curfile()
        Project.All.remove(self)

    def save_vars(self):
        vs = {}
        for vn in VARS:
            v = vim.vars.get(vn)
            if None != v:
                vs[vn] = v
        self.kvdb.set("vim_vars", vs)



    def save_curfile(self):
        fs = []
        for w in vim.windows:
            name = w.buffer.name
            if not name:
                continue

            if name.startswith(self.root):
                fs.append(name)

        self.kvdb.set("lastopen", fs)


    def add_c_include(self, path):
        "为工程增加 C 头文件路径"
        inc = self.kvdb.get("cinclude")
        if not isinstance(inc, list):
            inc = [path]
        else:
            if path in inc:
                return False
            else:
                inc.append(path)

        self.kvdb.set("cinclude", inc)
        self.kvdb.save()
        return True


def CInc(inc):
    path = utils.bufferpath()
    for p in Project.All:
        if path.startswith(p.root):
            break
    else:
        return

    p.add_c_include(inc)

def update_vim_vars(vs):
    if not isinstance(vs, dict):
        return

    for k, v in vs.items():
        vim.vars[k] = v




if __name__ == "__main__":
    pass

