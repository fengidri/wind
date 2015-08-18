# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-18 17:21:56
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim

@pyvim.cmd()
def Syntax():
    pyvim.echo(pyvim.syntax_area())

if __name__ == "__main__":
    pass

