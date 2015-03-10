# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-13 16:48:12
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import re
import os
import pyvim
from im import imutils
import logging


class IM_Path(object):
    "处理输入路径的情况"
    def __init__(self):
        self._path_regex = re.compile( """ 
          # 1 or more 'D:/'-like token or '/' or '~' or './' or '../'
          (?:[A-z]+:/|[/~]|\./|\.+/)+

          # any alphanumeric symbal and space literal
          (?:[/a-zA-Z0-9()$+_~.\x80-\xff-\[\]]|

          # skip any special symbols
          [^\x20-\x7E]|

          # backslash and 1 char after it. + matches 1 or more of whole group
          \\.)*$
          """, re.X )
        self.pmenu = pyvim.SelMenu()

        
    def im(self, key):
        s = imutils.key_to_see(key)
        if len(s)  != 1:
            return

        s = pyvim.str_before_cursor() + s

        
        logging.error(s)
        match = self._path_regex.search(s)
        if not match:
            return False
        logging.error('match')

        path = os.path.expanduser(match.group())
        path_dir = os.path.dirname(path)
        basename_l = os.path.basename(path).lower()
        l = len(basename_l)


        try:
            ns = os.listdir(path_dir)
            if l == 0:
                #当用户没有转入前缀时, 不显示隐藏文件名
                relative_dir = [p for p in ns if not p.startswith('.') ]
            else:
                #当用户输入了前缀的时候, 进行过滤, 并区分大小写
                relative_dir = [p for p in ns if
                        p.lower().startswith(basename_l) ]
        except:
            relative_dir = []

        imutils.key_feed(key)
        self.pmenu.showlist(relative_dir, l)
        


        return True


if __name__ == "__main__":
    pass

