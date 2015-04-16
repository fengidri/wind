# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 14:03:34
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import commands
import pyvim
import logging
from utils import paser


def runssh(path, command):
    p = paser(path)
    if not p:
        return None, None
    user, host, path = p
    cmd = 'ssh  -o ConnectTimeout=3 %s%s cd "%s && %s"' % (user, host, path, command)
    return commands.getstatusoutput(cmd)



def listdir(path):
    s, o = runssh(path, 'ls -L --color=never -1 -p')
    if s != 0:
        pyvim.echoline('ssh error: %s' % o)
        return None, None
    logging.error(o)

    lines = o.split('\n')
    fs = []
    dirs = []
    for line in lines:
        if line[-1] == '/':
            dirs.append(line[0:-1])
        else:
            fs.append(line)
    return (dirs, fs)

def realpath(path):
    return path

def pull(scp_path, tempfile):
    t = paser(scp_path)
    if not t:
        return
    user, host, path = t


    cmd = 'scp -o ConnectTimeout=3 %s%s:%s %s' % (user, host, path, tempfile)
    pyvim.echoline('start scp: %s' % scp_path)
    code, o  = commands.getstatusoutput(cmd)
    if code == 0:
        pyvim.echoline('Pull success: %s' % scp_path)
    else:
        logging.error(cmd)
        pyvim.echoline('Pull fail: %s' % scp_path, hl=True)
        return
    return tempfile

def push(tmp_file, scp_path):
    t = paser(scp_path)
    if not t:
        return
    user, host, path = t

    cmd = 'scp -o ConnectTimeout=3 %s  %s%s:%s ' % ( tmp_file, user, host, path)
    pyvim.echoline('start scp: %s' % scp_path)
    code, o  = commands.getstatusoutput(cmd)
    if code == 0:
        pyvim.echoline('Push success: %s' % scp_path)
    else:
        logging.error(cmd)
        pyvim.echoline('Push fail: %s' % scp_path, hl=True)




if __name__ == "__main__":
    pass

