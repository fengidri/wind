# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 12:23:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import utils
class EnterLine(utils.Object):
    def __init__(self, buf, linenu, prefix = ''):
        self.b = buf
        self.linenu = linenu
        self.b[linenu] = "%s:" % prefix
        self.col = len(prefix) + 1

    def focus(self):
        pass



if __name__ == "__main__":
    pass

