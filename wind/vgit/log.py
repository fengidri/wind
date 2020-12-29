# -*- coding:utf-8 -*-

import os

def log(n):
    cmd = 'git log --oneline --no-color -%d' % n
    o = []
    lines = os.popen(cmd).readlines()
    for line in lines:
        line = line.strip()
        o.append(line.split(' ', 1))

    return o



