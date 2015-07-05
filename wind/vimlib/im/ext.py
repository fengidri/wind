# -*- coding:utf-8 -*-
#    time      :   2015-06-30 14:59:52
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import imutils
import imrc
import logging
def start():
    imrc._feedkeys = imrc.Feedkeys()
    imrc.count += 1

def stop():
    imrc._feedkeys.feed()

imutils.add_hook('start', start)
imutils.add_hook('stop', stop)

if __name__ == "__main__":
    pass

