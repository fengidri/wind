# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-15 20:26:30
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import sys
import json
import logging

curdir = os.path.dirname(os.path.realpath(__file__))

plugin_path = os.path.join(curdir, 'plugin')
static_path = os.path.join(curdir, 'static')
site_packages = os.path.join(curdir, 'site-packages')

sys.path.insert(0, site_packages)
import cottle
from cottle import config
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s'
#       ,filename="/home/log/voscfg/voscfg.log"
        )

opts = {
        'plugin': plugin_path,
        'path_static' : static_path,
        'pre_static' : '/static'
        }



def main():
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 9480))
        sock.close()
    except Exception, e:
        print e
        cfg = config.config()
        cfg.host = "127.0.0.1"
        cfg.port = 9480
        application = app = cottle.Cottle(opts)
        app.run(cfg)

if __name__ == "__main__":
    main()


















