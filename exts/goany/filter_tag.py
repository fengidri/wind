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
    cmd = r"ctags --sort=no -f - -n --fields=-lzf --regex-c='/^SYSCALL_DEFINE[[:digit:]]?\(([^,)]+).*/syscall_\1/' %s" % filename
    f = os.popen(cmd)

    lines = f.readlines()
    f.close()
    tags = pyvim.parse_tags(lines)

    l = {'v':[], 'm':[], 'f':[]}

    for tag, v in tags.items():
        for f, cmd, ext in v:
            if not ext:
                continue

            t = ext[0]
            if t not in 'vmf':
                continue

            if len(ext) > 1:
                tag = "%s.%s" % (ext[1], tag)

            l[t].append((tag, cmd))

    for v in l.values():
        v.sort(key = lambda x:x[0])

    o = l['f']
    o.extend(l['v'])
    o.extend(l['m'])

    return zip(*o)

class tag_filter(object):
    INSTANCE = None
    def __init__(self):
        tag_filter.INSTANCE = self

        vim.command('update')
        tags_name, tags_lineno = ctag(vim.current.buffer.name)
        #tags.sort()
        self.win = Search(tags_name)
        self.tags_lineno = tags_lineno

        self.win.FREventBind("Search-Quit", self.quit)


    def quit(self, win, index):
        tag_filter.INSTANCE = None
        if None == index:
            return

        if index > -1:
            linenu = self.tags_lineno[index]
            if linenu:
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

