# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 12:15:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import sys
import redis
import json
from cottle import handle
from textohtml import html, markdown
import traceback

name = 'texshow'
urls = ('', "index",
        '/data', "data")

class index(handle):
    def GET(self):
        return self.template('texshow')

class data(handle):
    data = "-- no data --"
    tp   = ''
    index = 0
    request_type = ""
    def GET(self):
        qindex = self.query.get("index")
        tp = self.query.get("type", 'HTML').lower()
        if qindex and qindex == str(self.index) and tp == self.request_type:
            return [self.index, '', tp]

        self.request_type = tp

        data = self.data

        if tp == 'html':
            try:
                data = html(buf = self.data)
            except:
                data = "<pre>%s</pre>" % traceback.format_exc()

        elif tp == 'markdown':
            try:
                data = markdown(buf = self.data)
            except:
                data = "<pre>%s</pre>" % traceback.format_exc()

        return [self.index, data, tp]

    def POST(self):
        self.tp    =  self.forms.get('type')
        self.data  =  self.forms.get('data')
        self.index += 1
        return 'OK'


if __name__ == "__main__":
    pass
