# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-05 09:32:14
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
from frainui import SearchWIN

class FilterFile(object):
    def __init__(self):
        self.win = SearchWIN()


_INSTANCE = None

@pyvim.cmd()
def FileFilter():
    global _INSTANCE
    if not _INSTANCE:
        _INSTANCE = FilterFile()


if __name__ == "__main__":
    pass

