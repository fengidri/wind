# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 14:03:34
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import commands
import pyvim
import logging
import tempfile
def paser(path):
    t = path[6:].split('/', 1)
    if len(t) != 2:
        logging.error('scp: paser: fial: %s' % path)
        return
    host, path = t
    user = ''
    if host.find('@') > -1:
        user, host = host.split('@', 1)
        user = user + '@'
    return (user, host, path)


def runssh(path, command):
    p = paser(path)
    if not p:
        return None, None
    user, host, path = p
    cmd = 'ssh %s%s cd "%s;%s"' % (user, host, path, command)
    return commands.getstatusoutput(cmd)



def listdir(path):
    s, o = runssh(path, 'ls -L --color=never -1 -p')
    if s != 0:
        pyvim.echoline('ssh error: %s' % o)
        return ([], [])
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

def pull(scp_path):
    t = paser(scp_path)
    if not t:
        return
    user, host, path = t
    sf = scp_path.split('.')
    if len(sf) > 1:
        sf = '.' + sf[-1]
    else:
        sf = ''


    f = tempfile.mktemp(suffix = sf)

    cmd = 'scp  %s%s:%s %s' % (user, host, path, f)
    pyvim.echoline('start scp: %s' % scp_path)
    code, o  = commands.getstatusoutput(cmd)
    if code == 0:
        pyvim.echoline('pull success scp: %s' % scp_path)
    else:
        logging.error(cmd)
        pyvim.echoline('pull fail scp: %s' % scp_path)
        return
    return f

def push(tmp_file, scp_path):
    t = paser(scp_path)
    if not t:
        return
    user, host, path = t

    cmd = 'scp %s  %s%s:%s ' % ( tmp_file, user, host, path)
    pyvim.echoline('start scp: %s' % scp_path)
    code, o  = commands.getstatusoutput(cmd)
    if code == 0:
        pyvim.echoline('push success scp: %s' % scp_path)
    else:
        logging.error(cmd)
        pyvim.echoline('push fail scp: %s' % scp_path)




if __name__ == "__main__":
    pass

