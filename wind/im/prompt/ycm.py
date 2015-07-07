# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-07 11:14:51
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import im.prompt as prompt

@prompt.prompt('ycm')
def handle():
    return -4

@handle
def wubi(patten):
    pass


if __name__ == "__main__":
    pass

