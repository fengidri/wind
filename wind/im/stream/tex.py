# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-26 12:13:53
#    email     :   fengidri@yeah.net
#    version   :   1.0.1



import im.env as env
import im.imrc as imrc
import vim
import re

from . import wubi

class IM_Tex(wubi.IM_Wubi):
    fts = ['tex', 'plaintex', 'latex']

    def isenable(self):
        m = re.search(r'\\[a-z]*$', env.before)
        if m:
            return False
        else:
            return True


