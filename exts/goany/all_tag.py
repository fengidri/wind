# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-27 16:55:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# search all tag in project

import os
import pyvim
from frainui import Search
import vim

def get_tags():
    filename = vim.current.buffer.name
    if not filename:
        return

    filename = os.path.dirname(filename)
    while True:
        t = os.path.join(filename, 'tags')
        if os.path.isfile(t):
            return t
        else:
            filename = os.path.dirname(filename)
            if filename == '/':
                return
    return

def paser_tags(tags):
    infos = {}
    for line in open(tags).readlines():
        if line[0] == '!':
            continue
        tt = line.split('\t', 2)
        if not tt:
            continue

        o = tt[-1]

        tagfile = tt[1]
        pos = o.find(';"')
        if pos == -1:
            tagaddress = o[2:-2]
            name = tt[0]
        else:
            tagaddress = o[2:pos - 2]
            items = o[pos + 2:].split('\t')
            name = "%s.%s" %(items[-1][0:-1], tt[0])

        infos[name] = (tagfile, tagaddress)
    return infos




def get_all_tags():
    tags = get_tags()
    if not tags:
        return None, {}

    return tags, paser_tags(tags)




class tag_filter(object):
    INSTANCE = None
    def __init__(self):
        tag_filter.INSTANCE = self

        vim.command('update')

        self.root, self.tags = get_all_tags()
        self.root = os.path.dirname(self.root)

        tags = self.tags.keys()
        tags.sort()
        self.win = Search(tags)

        self.win.FREventBind("Search-Quit", self.quit)


    def quit(self, win, line):
        tag_filter.INSTANCE = None
        pyvim.log.error(line)
        if not line:
            return

        tt = self.tags.get(line)
        pyvim.log.error(tt)

        path = os.path.join(self.root, tt[0])
        vim.command("edit %s" % path)


        for i, line in enumerate(vim.current.buffer):
            if line == tt[1]:
                vim.current.window.cursor = (i + 1, 0)
                break

        pyvim.log.info("i got         : %s", tt[0])
        pyvim.log.info("i got pattern : %s", tt[1])
        #vim.current.window.cursor = (linenu, 0)

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



