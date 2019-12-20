# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-16 13:42:17
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import tempfile
import vim
import os

TEMPID = None
TEMPDIR = tempfile.mkdtemp()
TEMPFILES = {}

def get_proctol(path):
    t = path.split('://')
    if len(t) > 1:
        return t[0]
    else:
        return 'disk'

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

def mkstemp(path):
    global TEMPID
    global TEMPDIR
    if TEMPID == None:
        TEMPID = 1
    else:
        TEMPID += 1

    bs = "%03d_%s" % (TEMPID, os.path.basename(path))
    bs =  os.path.join(TEMPDIR, bs)

    TEMPFILES[bs]   = path
    TEMPFILES[path] = bs
    return bs

def tmpgetpath(tmp):
    return TEMPFILES.get(tmp)

def pathgettmp(path):
    return TEMPFILES.get(path)


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

def bufferpath(buf = None):
    if not buf:
        buf = vim.current.buffer

    #if buf.options['buftype'] != '':
    #    return

    path = buf.name

    t = tmpgetpath(path)
    if t:
        return t
    return path

if __name__ == "__main__":
    pass

