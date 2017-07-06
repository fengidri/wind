# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-14 13:43:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import urllib2
import urllib
import json
import pyvim
import requests
import vim
import os
################################################################################
# 连接服务器
################################################################################
from textohtml import html


import units

INDEX = os.path.join(os.getcwd(), "store/index.json")

class Remote(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Remote, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if hasattr(self, "map_id_tmp_file"):
            return

        self.map_id_tmp_file = {}
        self.news = []
        self.load_list()

    def get_id_by_name(self, name): # 返回的ID 是str
        if name in self.news:
            return None

        for ID, _f in self.map_id_tmp_file.items():
            if _f == name:
                return str(ID)

    def update(self, ID, name):
        ID = str(ID)
        if name in self.news:
            self.news.remove(name)

        self.map_id_tmp_file[ID] = name


    def load_list(self):
        info = open(INDEX).read()
        info = json.loads(info)

        for v in info.values():
            if not v.get('title'):
                v['title'] = 'undefined'

            if not v.get('post'):
                v['post'] = '1'

        self.info = info

    def iter(self):
        keys = [int(k) for k in self.info.keys()]
        keys.sort()
        keys.reverse()
        for k in keys:
            yield str(k), self.info[str(k)]


    def load_tex(self, ID_s):
        tmp = self.map_id_tmp_file.get(ID_s)
        if tmp:
            return tmp

        url = units.URL_CHAPTER % (units.SERVER, ID_s)
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req).read()
        except Exception, e:
            pyvim.echo(e, hl=True)
            return

        tmp = units.tmpfile()
        open(tmp, 'wb').write(res)
        self.map_id_tmp_file[ID_s] = tmp
        return tmp

    def post_tex(self, tex, name): # 返回的 ID 是 int
        j = { 'tex': tex }

        if units.URL_CHAPTER.endswith('.mkiv'):
            try:
                j['html'] = html(buf = tex)
            except Exception, e:
                pyvim.echo(str(e), hl=True)
                return

        ID = self.get_id_by_name(name)
        if ID:
            method = "PUT"
            uri = units.URL_PUT % (units.SERVER, ID)
        else:
            method = "POST"
            uri = units.URL_POST % units.SERVER

        headers = {'Content-Type': "application/json"};

        res = requests.request(method, uri, headers=headers, data=json.dumps(j))
        return int(res.text)





if __name__ == "__main__":
    pass

