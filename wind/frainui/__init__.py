# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:15:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from node import Node, Leaf
from listwin import LIST
import logging
import utils

def inputstream(key):
    logging.error('inputstream: %s' % key)

def handle(name, ev):
    """
        @paser: name ui object name
        @ev:    method of the object
    """
    obj = utils.Objects.get(name)
    if not obj:
        return

    if not hasattr(obj, ev):
        return

    getattr(obj, ev)()

    #if event == "list-refresh":
    #    LIST().refresh()

    #elif event == "list-open":
    #    LIST().open()

    #elif event == "list-close":
    #    LIST().close()
