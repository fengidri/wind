# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-18 10:17:45
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import filter_tag
import filter_file
import all_tag
import tags


import pyvim
@pyvim.cmd(complete = ['file', 'tag'])
def GoAny(f, o=None):
    if f == 'file':
        filter_file.FileFilter()

    elif f == 'tag':
        if o == None:
            pyvim.each('Nead Option')
            return

        if o == 'file':
            filter_tag.TagFilter()

        elif o == 'all':
            all_tag.TagFilter()

        elif o == 'jump':
            tags.Tag()

        elif o == 'back':
            tags.TagBack()

        elif o == 'refresh':
            tags.TagRefresh()

if __name__ == "__main__":
    pass

