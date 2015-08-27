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

def ctag(filename):
    cmd = "ctags --sort=no -f - -n --fields=-lzf %s" % filename
    f = os.popen(cmd)

    tags = {}

    for line in f.readlines():
        tmp = line.split()

        keyword        = tmp[0] #tag name
        tp             = tmp[3] # 类型如 f
        linenu         = int(tmp[2][0: -2])# 行号, ctag 输出如: 114;"
        if not tp in 'fvm':
            continue

        if tp == 'm':
            keyword = "%s.%s" %(tmp[4], keyword)

        tags[keyword] = linenu

    return tags

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
        tt = line.split('\t')
        if not tt:
            continue
        infos[tt[0]] = line
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
        if not line:
            return

        line = self.tags.get(line)
        if not line:
            return

        tt = line.split('\t')
        if len(tt) < 3:
            return

        tt[1] = os.path.join(self.root, tt[1])
        vim.command("edit %s" % tt[1])

        try:
            vim.command(tt[2])
        except:
            pass

        pyvim.log.info("i got         : %s", tt[1])
        pyvim.log.info("i got pattern : %s", tt[2])
        #vim.current.window.cursor = (linenu, 0)

    def show(self):
        pyvim.log.error('call show')
        self.win.BFToggle()


@pyvim.cmd()
def TagFilter():
    if not vim.current.buffer.name:
        return

    if tag_filter.INSTANCE:
        tag_filter.show()
        return

    tag_filter()


if __name__ == "__main__":
    pass

