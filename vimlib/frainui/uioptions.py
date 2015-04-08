# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 10:41:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import data
import core


def gotowin():
    if data.LISTWIN and data.LISTWIN.valid():
        vim.current.window = data.LISTWIN.win
    else:
        createwin()



if __name__ == "__main__":
    pass

