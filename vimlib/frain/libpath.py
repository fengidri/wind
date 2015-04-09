# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 14:09:44
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import vim
basename = os.path.basename
join     = os.path.join
realpath = os.path.realpath

def listdir(path):
    names = os.listdir(path)
    dirs = []
    fs = []
    for n in names:
        p = os.path.join(path, n)
        if os.path.isdir(p):
            dirs.append(n)
        else:
            fs.append(n)
    return (dirs, fs)

def bufferpath(buf = None):
    if not buf:
        buf = vim.current.buffer
    if buf.options['buftype'] != '':
        return
    path = buf.name
    if not path:
        return
    return path


def getnames(root, path):  # 得到用于frainui 进行分析的names
    if not path.startswith(root):
        return
    base = os.path.basename(root)
    p = len(root) - 1
    if root[-1] != '/':
        p += 1
    p = path[p+1:]
    names = p.split('/')
    names.insert(0, base)
    return names



if __name__ == "__main__":
    pass
