# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-18 19:29:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import json

class KvCache(object):
    Singleton = False
    DBFile = os.path.join(os.environ.get("HOME"), '.vim/config/kv.db')
    def __init__(self):
        dbdir = os.path.dirname(self.DBFile)
        if not os.path.exists(dbdir):
            os.makedirs(dbdir)
        self.data = self._load()

    def __new__(cls, *args, **kw):
        if not cls.Singleton:
            return super(KvCache, cls).__new__(cls, *args, **kw)
        if not hasattr(cls, '_instance'):
            orig = super(KvCache, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def _load(self):
        try:
            c = open(self.DBFile).read()
            return json.loads(c)
        except:
            return {}

    def _save(self, se):
        open(self.DBFile, 'w').write(json.dumps(se))

    def get(self, k, ns = None):
        space = self.data.get(ns)
        if not space:
            return None

        v = space.get(k)
        if not v:
            return None

        data = v.get('data')
        if not data:
            return None

        return data

    def set(self, k, v, ns = None):
        space = self.data.get(ns)
        if not space:
            self.data[ns] = {k: {"data": v}}

        else:
            space[k] = {"data": v}

    def save(self):
        self._save(self.data)


    def getcurfile(self):
        fs = {}
        for w in vim.windows:
            name = w.buffer.name
            if not name:
                continue
            for path in pyvim.Roots:
                if name.startswith(path):
                    l = fs.get(path)
                    if l == None:
                        fs[path] = [name]
                    else:
                        l.append(name)
                    break
        return fs



if __name__ == "__main__":
    pass
