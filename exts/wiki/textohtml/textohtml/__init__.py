# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:15:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

#TODO  最后的一个text会没有输出

import logging

import codecs

#logging.basicConfig(level = logging.DEBUG, format = '%(message)s')
logging.basicConfig(level = logging.ERROR, format = '%(message)s')

from words import split
from nodes import node_tree
from pre import prehandler
from paragraph import SplitParagraph

def handle(f=None, buf=None):
    if f:
        buf = codecs.open(f, 'r','utf8').read()

    if not buf:
        return

    ws = prehandler(split(buf))
    return SplitParagraph(ws, 0)


def markdown(path=None, buf=None):
    ws = handle(path, buf)
    if not ws:
        return ''

    return ws.md()

def html(path=None, buf=None):
    ws = handle(path, buf)
    if not ws:
        return ''

    return ws.html()

def texstohtml(src, o):
    import traceback
    try:
        words = prehandler(split(src))
        html = SplitParagraph(words, 0).html()
    except:
        html = '<pre>%s</pre>' % traceback.format_exc()


    f = codecs.open(o, 'w','utf8')
    f.write(html)

if __name__ == "__main__":
    pass

