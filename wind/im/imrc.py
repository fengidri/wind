# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-10 18:15:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import os
import string
import pyvim
from pyvim import log
import imutils

count = 0  #
_feedkeys = None

@imutils.hook('start')
def start():
    global _feedkeys
    global count
    _feedkeys = Feedkeys()
    count += 1

@imutils.hook('stop')
def stop():
    _feedkeys.feed()

class IMRedirectStop(Exception):
    pass

class Feedkeys(object):
    def __new__(cls, *args, **kw):
        "单例模式"
        if not hasattr(cls, '_instance'):
            orig = super(Feedkeys, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            Feedkeys._feed_ = []
        return cls._instance
    def __init__(self):
        del Feedkeys._feed_[:]

    def append(self, k):
        Feedkeys._feed_.append(k)

    def feed(self):
        log.error('feed:%s', Feedkeys._feed_)
        pyvim.feedkeys(Feedkeys._feed_)

def feedkeys(k):
       _feedkeys.append(k)


