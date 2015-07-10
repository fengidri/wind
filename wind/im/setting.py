# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-07 17:54:45
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import imrc
from pyvim import log
import rc
def handle(key, value):
    if key == "wubi":
        if value == 'true':
            rc.IM_Wubi = True
        else:
            rc.IM_Wubi = False
        log.error("IM Setting: %s: %s", key, value)


if __name__ == "__main__":
    pass

