#encoding:utf8
import os
import sys
import logging
import pyvim
import vim
from imutils import key_all, key_feed, emit_event
import imrc
from plugins import Plugins



class Input_Monitor(object):
    def load_ftmode(self, m):
        if not hasattr(m, 'im_ft'):
            return

        f = m.im_ft()

        for ft in f.im_ft:
            self.ftmode[ft] = f

    def __init__(self):
        self.ftmode = {} # 记录每一种文件类型对应的处理类

        ftpath = os.path.realpath(__file__)
        ftpath = os.path.dirname(ftpath)
        ftpath = os.path.join(ftpath, 'filetype')

        self.plugins = Plugins(ftpath)
        self.plugins.hook_init = self.load_ftmode
        self.plugins.loads()

        for ft, cls in self.ftmode.items():
            logging.error('%s: %s' % (ft, cls))



    def im( self, key ):
        emit_event('start')
        imrc.feedkeys = imrc.Feedkeys()

        imrc.count += 1#记数器, 统计输入
        ft = vim.eval('&ft')

        im = self.ftmode.get(ft, None)# 按照文件类型得到对应的filetype 处理方法

        emit_event('ft_pre')

        if im == None:
            key_feed(key)
        else:
            im.im(key)
        emit_event('ft_post')

        imrc.feedkeys.feed()
        emit_event('stop')

    def init_monitor_keys( self ):
        keys=key_all()
        for map_key, name in keys:
            command='inoremap <expr> %s Input_Monitor( "%s" )' % ( map_key, name)
            vim.command(command)

