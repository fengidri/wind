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
        ('%d ' % os.getpid())  +
        '%(filename)s:%(lineno)d %(levelname)s: %(message)s')
handlers.setFormatter(formatter)

log = logging.getLogger("wind")
#log.setLevel(logging.INFO)
log.setLevel(logging.error)
#log.setLevel(logging.DEBUG)
log.addHandler(handlers)


log.error(">>>>>>>>>>>>>>> VIM Start <<<<<<<<<<<<<")

def excepthook(type, value, trace):
    if type == KeyboardInterrupt:
        print ""
        return

    pyvim.echoline(">>Error(%s): %s: " % (LOGFILE, type.__name__ + str(value)))
    log.error("Uncaught exception:", exc_info =(type, value, trace))

sys.excepthook = excepthook


import pyvim
from im import IM

ftpath = os.path.realpath(__file__)
ftpath = os.path.dirname(ftpath)
exts_path = os.path.join(ftpath, '../exts')
def load_ext():
    from plugins import Plugins
    Plugins(exts_path).loads()

if __name__ != "__main__":
    load_ext()

