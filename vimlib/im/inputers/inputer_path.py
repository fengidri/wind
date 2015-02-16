# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-13 16:48:12
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import re
import os
import pyvim
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

        if len(key) != 1:
            return False

        s = pyvim.str_before_cursor() + key

        match = self._path_regex.search(s)
        if not match:
            return False

        path = os.path.expanduser(match.group())
        path_dir = os.path.dirname(path)
        basename = os.path.basename(path)
        l = len(basename)


        try:
            relative_dir = [p for p in os.listdir(path_dir) if
                    p.startswith(basename) ]
        except:
            relative_dir = []

        pyvim.feedkeys(key, 'n')
        self.pmenu.showlist(relative_dir, l)
        


        return True


if __name__ == "__main__":
    pass

