# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-07 11:14:51
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import im.prompt as prompt
import im.env as env
import string


@prompt.prompt('ycm')
def handle():
    if not env.before:
        return -3

    last_c = ord(env.before[-1])

    if last_c >= 0x61 and last_c <= 0x7a: # lower
        return -4

    if last_c == 0x2e or last_c == 0x3e or last_c == 0x5f: #  . > _
        return -4

    if last_c < 0x41:
        return -3

    if last_c  <=  0x5a: # upper
        return -4

    return -4

@handle
def base(patten):
    pass


if __name__ == "__main__":
    pass

