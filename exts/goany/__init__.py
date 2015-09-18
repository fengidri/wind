# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-18 10:17:45
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import filter_tag
import filter_file
import all_tag


import pyvim
@pyvim.cmd(complete = ['file', 'tag'])
def GoAny(f):
    if f == 'file':
        filter_file.FileFilter()

    elif f == 'tag':
        filter_tag.TagFilter()

    elif f == 'Tag':
        all_tag.TagFilter()

if __name__ == "__main__":
    pass

