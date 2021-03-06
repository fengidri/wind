# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-01-22 12:22:31
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from .wbtree import ROOT

def wbsearch(patten):
    try:
        node =  ROOT.wb_find(patten)
        return (node.wb_words(), node.wb_associate())
    except:
        return ([], [])

def wbsetcount(patten, word):
    try:
        node =  ROOT.wb_find(patten)
    except:
        return None
    node.addcount(patten, word)

if __name__ == "__main__":
    pass

