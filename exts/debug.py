# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-08 17:39:14
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from pyvim import log
from pyvim import cmd
import logging

subcmd = ['notset', 'info', 'error', 'debug', 'warning', 'critical']

@cmd(complete = subcmd)
def Debug(level):
    if not level in subcmd:
        return

    level = level.upper()
    if not hasattr(logging, level):
        return

    level = getattr(logging, level)
    log.setLevel(level)


    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')



if __name__ == "__main__":
    pass

