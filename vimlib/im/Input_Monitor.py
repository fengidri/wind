#encoding:utf8
import os
import sys
import logging
import pyvim
import vim
from imutils import key_all, key_feed
import imrc



class Input_Monitor(object):
    def __init__(self):
        self.ftmode = {} # 记录每一种文件类型对应的处理类 

        ftpath = os.path.realpath(__file__)
        ftpath = os.path.dirname(ftpath)
        ftpath = os.path.join(ftpath, 'filetype')
        mds = os.listdir(ftpath)
        logging.error(mds)
        sys.path.insert(0, ftpath)
        for m in mds:
            if not m.endswith('.py'):
                continue
            if m.startswith('.'):
                continue
            try:
                md = __import__(m[0:-3])
                logging.error(md)
                self.load_ftmode(md)
            except Exception, e:
                logging.exception(e)

                continue

        del sys.path[0]

        logging.debug("Input Mointer: ftmode: %s", self.ftmode)
    


    def load_ftmode(self, m):
        if not hasattr(m, 'im_ft'):
            return
        f = m.im_ft()

        for ft in f.im_ft:
            self.ftmode[ft] = f 


    def im( self, key ):
        imrc.count += 1#记数器, 统计输入
        ft = vim.eval('&ft')

        im = self.ftmode.get(ft, None)# 按照文件类型得到对应的filetype 处理方法

        logging.debug("Input Mointer:%s %s", key, im)

        if im == None:
            key_feed(key)
        else:
            im.im(key)

    def init_monitor_keys( self ):
        keys=key_all()
        for map_key, name in keys:
            command='inoremap <expr> %s Input_Monitor( "%s" )' % ( map_key, name)
            vim.command(command)

