# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-09 09:29:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

"""
The Entry for Wind project. Just need import.
"""
import os
import sys
import logging
import logging.handlers
LOGFILE = "/tmp/vimlog"
MAXBYTES = 1024 * 1024 * 10

logging.basicConfig(filename="/dev/null", level=logging.DEBUG)

handlers = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=MAXBYTES)
#formatter = logging.Formatter('>>%(levelname)s: %(message)s')
formatter = logging.Formatter(
        ('>> %d ' % os.getpid())  +
        '%(filename)s:%(lineno)d %(levelname)s: %(message)s')
handlers.setFormatter(formatter)

log = logging.getLogger("wind")

# level
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
log.setLevel(logging.ERROR)

log.addHandler(handlers)


log.error(">>>>>>>>>>>>>>> VIM Start <<<<<<<<<<<<<")

import pyvim

def excepthook(type, value, trace):
    if type == KeyboardInterrupt:
        print("")
        return

    pyvim.echoline(">>Error(%s): %s: " % (LOGFILE, type.__name__ + str(value)))
    log.error("Uncaught exception:", exc_info =(type, value, trace))

sys.excepthook = excepthook


import im
IM = im.IM
im.stream.Init()
tips = im.tips


def load_ext():
    from plugins import Plugins

    ftpath = os.path.realpath(__file__)
    ftpath = os.path.dirname(ftpath)
    exts_path = os.path.join(ftpath, '../exts')

    Plugins(exts_path).loads()


import importlib
def load_plugin(name, path):
    sys.path.insert(0, path)
    importlib.import_module(name)

    #import importlib.util

    #path = os.path.join(path, name)

    #spec = importlib.util.spec_from_file_location(name, path)
    #foo = importlib.util.module_from_spec(spec)
    #spec.loader.exec_module(foo)


    #l = importlib.find_loader(name, path)
    #if not l:
    #    print('not find loader %s from %s' % (name, path))
    #l.load_module()

