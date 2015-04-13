# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 14:09:44
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import vim
import libpathscp
import logging
import tempfile
basename = os.path.basename
join     = os.path.join
realpath = os.path.realpath


TEMPID = None
TEMPDIR = tempfile.mkdtemp()
def mkstemp(path):
    global TEMPID
    global TEMPDIR
    if TEMPID == None:
        TEMPID = 1
    else:
        TEMPID += 1

    bs = "%03d_%s" % (TEMPID, basename(path))
    return os.path.join(TEMPDIR, bs)


TEMPFILES = {}

def get_proctol(path):
    if path.startswith('scp://'):
        return libpathscp
    else:
        return

def realpath(path):
    if get_proctol(path):
        return path
    return os.path.realpath(path)


def listdir(path):
    pt = get_proctol(path)
    if pt:
        return pt.listdir(path)

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

    t = TEMPFILES.get(path)
    if t:
        return t
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

def editfile(path):
    return pt.editfile(path)


def pull(path):
    pt = get_proctol(path)
    if not pt:
        return path
    f = pt.pull(path, mkstemp(path))
    if f:
        TEMPFILES[f] = path
        return f

def push():
    path = vim.current.buffer.name

    logging.debug('push %s' % path)

    tp = TEMPFILES.get(path)
    if not tp: return

    pt = get_proctol(tp)
    if not tp:
        return
    pt.push(path, tp)

if __name__ == "__main__":
    pass

