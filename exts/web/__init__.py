# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-10-16 07:17:40
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
def start():
    curfile = os.path.realpath(__file__)
    curdir  = os.path.dirname(curfile)
    fwebdir = os.path.join(curdir, 'fweb')
    os.popen2('cd %s; python2 fweb.py >/dev/null 2>&1' % fwebdir)
#    os.popen2('cd %s; python2 fweb.py 2>&1 >/tmp/fweb.log' % fwebdir)


start()

if __name__ == "__main__":
    pass

