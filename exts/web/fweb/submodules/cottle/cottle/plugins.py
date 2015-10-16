# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-18 17:53:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import sys
import os
import re
import logging
def load(path):
    sys.path.insert(0, path)

    modes = os.listdir( path )
    infos = __load(modes)

    del sys.path[0]
    return infos


def __load(modes):
    regex = '^([\w\d]+)\.py$'
    mode_infos = {}
    for mode in modes:
        match = re.search(regex, mode)
        if not match: continue

        try:
            modename = match.group(1)
            mode = __import__(modename)
            mode_info = __mode_init(mode)
            if mode_info:
                mode_infos[modename] = mode_info
            logging.info("load plugin: %s" % modename)
        except IOError, why:
             logging.error("Load plugin Error:%s:%s" %( mode, why))
    return mode_infos

def __mode_init(mode):
    mode_info  = [mode]

    attr = 'urls'
    if not hasattr(mode, attr):
        logging.error('mode init:%s not hasattr [urls]' % (mode, attr))
        return []
    urls = getattr(mode, attr)

    attr = 'name'
    if not hasattr(mode, attr):
        name = mode.__name__
    else:
        name = getattr(mode, attr)

    return (mode, name, urls)














