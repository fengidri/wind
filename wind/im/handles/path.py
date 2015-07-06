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
from pyvim import log as logging
import im.prompt as prompt

def get_match_names(path_dir, basename):
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



def try_abbreviation(path):
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
            rel = get_match_names(f, abb)
            for r in rel:
                fan.append(os.path.join(f, r))
        fa = fan
    self.pmenu.showlist(fa, len(path))
    return True

def findstart():
    return True

def base():
    path = os.path.expanduser(match.group())
    path_dir = os.path.dirname(path)

    if not os.path.isdir(path_dir):
        return self.try_abbreviation(path)

    basename = os.path.basename(path)
    l = len(basename)
    get_match_names(path_dir, basename)


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

    def im_lower(self, key):

        s = pyvim.str_before_cursor() + key

        match = self._path_regex.search(s)
        if not match:
            return False

        feedkeys(key)
        prompt.active(findstart, base)
        return True

    im_digit = im_upper = im_punc = im_lower



if __name__ == "__main__":
    pass





























