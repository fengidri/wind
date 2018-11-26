# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-19 04:35:02
#    email     :   fengidri@yeah.net
#    version   :   1.0.1



import pyvim

def handle(*args):
    # 目前用于在 cursor hold 的时候触发补全
    # 不使用 CursorHoldI 事件是由于这事件触发时间比较长 4000ms
    # 同时这个时间还用于 swap, 并不方便修改

    s = pyvim.pyvim.str_before_cursor()
    if len(s) < 2:
        return

    if not s[-1].isalpha():
        return

    pyvim.feedkeys(('\<C-c>', 'm'))
