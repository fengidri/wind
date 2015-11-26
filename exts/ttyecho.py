# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-08 11:43:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim
import os


@pyvim.cmd()
def TTYrun(*k):
    os.popen2("ttyrun %s" % ' '.join(k))

