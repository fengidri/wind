# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-05 09:32:14
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
from frainui import Search
import vim


def getfiles(path):
    lines = []
    lenght = len(path)
    if path[-1] != '/':
        lenght += 1

    for root, ds, fs  in os.walk(path):
        ds[:] = [d for d in ds if d[0] != '.']
        for f in fs:
            if f[0] == '.':
                continue

            suffix = f.split('.')
            if len(suffix) > 1:
                suffix = suffix[-1]
                if suffix in ['o', 'so', 'pyc', 'lo']:
                    continue

            f = os.path.join(root, f)
            lines.append(f[lenght:])

    for b in vim.buffers:
        name = b.name
        if name.startswith(path):
            name = name[lenght:]
            if name in lines:
                lines.remove(name)
                lines.insert(0, name)

    return lines




class file_filter(object):
    INSTANCE = None
    def __init__(self, path):
        file_filter.INSTANCE = self

        self.path = path

        self.win = Search(getfiles(path))
        self.win.FREventBind("Search-Quit", self.quit)


    def quit(self, win, line):
        file_filter.INSTANCE = None

        if line:
            path = os.path.join(self.path, line)
            pyvim.log.info("i got : %s", path)

            vim.command("update")
            vim.command("edit %s" % path)

    def show(self):
        pyvim.log.error('call show')
        self.win.BFToggle()


def FileFilter():
    if not vim.current.buffer.name:
        return

    if file_filter.INSTANCE:
        file_filter.INSTANCE.show()
        return

    name = vim.current.buffer.name
    root = None
    for r in pyvim.Roots:
        if not name:
            root = r
            break

        if name.startswith(name):
            root = r
            break
    else:
        pyvim.echo("Not Found root in pyvim.Roots for current file.", hl=True)
        return

    if root:
        file_filter(root)



if __name__ == "__main__":
    pass

