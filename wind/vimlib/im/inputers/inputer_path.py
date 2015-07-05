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
from im.imrc import feedkeys


class IM_Path(object):
    "处理输入路径的情况"
    def __init__(self):
        self._path_regex = re.compile( """
          # 1 or more 'D:/'-like token or '/' or '~' or './' or '../'
          (?:[A-z]+:/|[/~]|\./|\.+/)

          # any alphanumeric symbal and space literal
          (?:[a-zA-Z0-9()$+_~.\x80-\xff-\[\]]|

          # skip any special symbols
          [^\x20-\x7E]|

          # backslash and 1 char after it. + matches 1 or more of whole group
          \\.)+

          # any alphanumeric symbal and space literal
          (?:[/a-zA-Z0-9()$+_~.\x80-\xff-\[\]]|

          # skip any special symbols
          [^\x20-\x7E]|

          # backslash and 1 char after it. + matches 1 or more of whole group
          \\.)*$
          """, re.X )
        self.pmenu = pyvim.SelMenu()
    def get_match_names(self, path_dir, basename):
        basename = basename.lower()
        try:
            ns = os.listdir(path_dir)
            if basename == '':
                #当用户没有转入前缀时, 不显示隐藏文件名
                relative_dir = [p for p in ns if not p.startswith('.') ]
            else:
                #当用户输入了前缀的时候, 进行过滤, 并区分大小写
                relative_dir = [p for p in ns if
                        p.lower().startswith(basename) ]
        except:
            relative_dir = []

        return relative_dir


    def im(self, key):
        s = imutils.key_to_see(key)
        if len(s)  != 1:
            return

        s = pyvim.str_before_cursor() + s


        match = self._path_regex.search(s)
        if not match:
            return False
        feedkeys(key)
        # path complete start

        path = os.path.expanduser(match.group())
        path_dir = os.path.dirname(path)

        if not os.path.isdir(path_dir):
            return self.try_abbreviation(path)

        basename = os.path.basename(path)
        l = len(basename)
        relative_dir = self.get_match_names(path_dir, basename)

        self.pmenu.showlist(relative_dir, l)
        return True

    def try_abbreviation(self, path):
        # 路径缩写补全: /u/l/b ===> /usr/local/bin
        if path.startswith('/'):
            fa = ['/']
            abbs = path.split('/')[1:]

        elif path.startswith('.'):
            fa = ['./']
            abbs = path.split('/')[1:]

        elif path.startswith('..'):
            fa = ['../']
            abbs = path.split('/')[1:]

        else:
            fa = [os.getcwd()]
            abbs = path.split('/')

        for abb in abbs:
            fan = []
            for f in fa:
                rel = self.get_match_names(f, abb)
                for r in rel:
                    fan.append(os.path.join(f, r))
            fa = fan
        self.pmenu.showlist(fa, len(path))
        return True






if __name__ == "__main__":
    pass





























