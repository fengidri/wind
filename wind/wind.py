# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-09 09:29:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

"""
The Entry for Wind project. Just need import.
"""
import os
from im import IM

ftpath = os.path.realpath(__file__)
ftpath = os.path.dirname(ftpath)
exts_path = os.path.join(ftpath, '../exts')

def load_ext():
    from plugins import Plugins
    Plugins(exts_path).loads()

if __name__ != "__main__":
    load_ext()

