# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-16 14:06:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
realpath = os.path.realpath

def realpath(path):
#    path = os.path.expanduser(path)
#    path = os.path.realpath(path)

    if not os.path.exists(path):
        return None

    if not os.path.isdir(path):
        return os.path.dirname(path)

    return path

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

if __name__ == "__main__":
    pass

