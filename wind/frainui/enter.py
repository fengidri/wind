# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 12:23:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import utils
import im
class EnterLine(utils.Object, im.keybase.BaseEnd):
    def __init__(self, buf, linenu, prefix = ''):
        self.b = buf
        self.linenu = linenu
        self.b[linenu] = "%s:" % prefix
        self.col = len(prefix) + 1
        self.Buffer = buf





if __name__ == "__main__":
    pass

