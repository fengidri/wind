# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 14:09:44
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
basename = os.path.basename
join     = os.path.join

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

