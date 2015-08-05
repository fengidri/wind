# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-05 09:32:14
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
from frainui import SearchWIN
import vim

def getfiles(path):
    cmd = 'cd {path}; find . {filter} 2>/dev/null'
    fs = [
            " -type d -name '.*' -prune -o ",
            " -type f  ! -name '.*' -and ",
            " -type f  ! -name '*.o' -and ",
            " -type f  ! -name '*.so' ",
            " -print "
            ]
    cmd = cmd.format(path = path, filter = ''.join(fs))
    pyvim.log.error("cmd: %s", cmd)

    return os.popen(cmd).readlines()

def getfiles(path):
    lines = []
    lenght = len(path)
    if path[-1] != '/':
        lenght += 1
    for root, ds, fs  in os.walk(path):
        ds = [d for d in ds if d[0] != '.']
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
    return lines


class FilterFile(object):
    def __init__(self, path):
        self.edit_win = vim.current.window

        self.path = path
        lines = getfiles(path)

        self.win = SearchWIN(lines)
        self.win.FREventBind("quit", self.quit)


    def quit(self, win, line):
        global _INSTANCE
        _INSTANCE = None

        count = vim.current.window.number
        vim.current.window = self.edit_win
        vim.command("%swincmd q" % count)
        if line:
            path = os.path.join(self.path, line)
            vim.command("edit %s" % path)
            vim.command("doautocmd BufRead")

        #vim.command("quit")

        #if line:
        #    path = os.path.join(self.path, line)
        #    pyvim.log.error("i got : %s", path)
#       #     vim.command("stopinsert")
        #    vim.command("e %s" % path)


_INSTANCE = None

@pyvim.cmd()
def FileFilter():
    global _INSTANCE
    if not _INSTANCE:
        name = vim.current.buffer.name
        for r in pyvim.Roots:
            if name.startswith(name):
                _INSTANCE = FilterFile(r)
                return
        else:
            pyvim.echo("Not Found root in pyvim.Roots for current file.",
                    hl=True)


if __name__ == "__main__":
    pass

