# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 14:09:44
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import vim
import logging
import tempfile
import utils

import libpathscp
import libpathdisk

procts = {
        'scp': libpathscp,
        'disk': libpathdisk
        }

basename = os.path.basename
join     = os.path.join




def get_proctol(path):
    pn = utils.get_proctol(path)
    p =  procts.get(pn)
    if p == None:
        raise Exception('dont know the proctol: %s'% pn)
    return p


def realpath(path):
    return get_proctol(path).realpath(path)


def listdir(path):
    return get_proctol(path).listdir(path)



def pull(path):
    pt = get_proctol(path)
    if pt == libpathdisk:
        return path

    tf = utils.pathgettmp(path)
    if tf:
        return tf

    f = pt.pull(path, utils.mkstemp(path))
    if f:
        return f

def push():
    path = vim.current.buffer.name

    tp = utils.pathgettmp(path)
    if not tp: return

    get_proctol(tp).push(path, tp)

if __name__ == "__main__":
    pass

