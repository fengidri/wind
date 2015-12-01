# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-06 19:08:33
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
from frainui import Search
import vim

def ctag(filename):
    cmd = "ctags --sort=no -f - -n --fields=-lzf %s" % filename
    f = os.popen(cmd)

    lines = f.readlines()
    f.close()
    tags = pyvim.parse_tags(lines)
    _tags = {}
    for k, v in tags.items():
        ext = v[2]
        if not ext:
            continue
        t = ext[0]
        if t not in 'vmf':
            continue

        if len(ext) > 1:
            k = "%s.%s" % (ext[1], k)

        _tags[k] = v[1]
    return _tags

class tag_filter(object):
    INSTANCE = None
    def __init__(self):
        tag_filter.INSTANCE = self

        vim.command('update')
        self.tags = ctag(vim.current.buffer.name)

        tags = self.tags.keys()
        tags.sort()
        self.win = Search(tags)

        self.win.FREventBind("Search-Quit", self.quit)


    def quit(self, win, line):
        tag_filter.INSTANCE = None
        if line:
            linenu = self.tags.get(line)
            if linenu:
                pyvim.log.info("i got : %s %s", line, linenu)
                vim.current.window.cursor = (linenu, 0)

    def show(self):
        pyvim.log.error('call show')
        self.win.BFToggle()


def TagFilter():
    if not vim.current.buffer.name:
        return

    if tag_filter.INSTANCE:
        tag_filter.show()
        return

    tag_filter()


if __name__ == "__main__":
    pass

