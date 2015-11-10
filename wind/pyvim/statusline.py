# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-11-10 08:09:58
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
STATUS = {}


def sl_set(name, value):
    STATUS[name] = value
    sl_update()

def sl_clear(name, value):
    if name in STATUS:
        del STATUS[name]

def sl_update():
    s = ' '.join(STATUS.values())
    vim.vars["pyvim_status_line_info"] = s


if __name__ == "__main__":
    pass


