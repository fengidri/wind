# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-21 10:59:34
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


from kvcache import KvCache
import os
import vim
import gitinfo
import json
import logging
import pyvim

class Project(object):
    All = []
    cincs = {}
    @classmethod
    def emit(cls, single):
        func = 'Hook_%s' % single
        logging.error(func)

        if hasattr(cls, func):
            getattr(cls, func)()

    @classmethod
    def Hook_FrainEntry(cls):
        cins = {}
        for p in cls.All:
            incs = p.kvdb.get("cinclude")
            if incs:
                cins[p.root] = incs

        if cins:
            vim.vars['frain_include_dirs'] = json.dumps(incs)

            # try cache Ycm's flag cache
            vim.command('silent YcmCompleter ClearCompilationFlagCache')

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


    def __init__(self, root, name = ''):
        self.root = root
        self.name = name
        self.kvdb = KvCache(os.path.join(self.root, '.wind'))
        self.info = gitinfo.gitinfo(root)
        Project.All.append(self)


    def save_curfile(self):
        fs = []
        for w in vim.windows:
            name = w.buffer.name
            if not name:
                continue

            if name.startswith(self.root):
                fs.append(name)

        self.kvdb.set("lastopen", fs)
        self.kvdb.save()



if __name__ == "__main__":
    pass

