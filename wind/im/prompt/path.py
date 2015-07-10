# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-13 16:48:12
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

"""
    /usr/lib/lib ->
                   libpng.so
                   libncursor.so
    /u/l/       ->
                   /usr/lib
                   /usr/local
"""

import re
import os

from pyvim import log
import im.prompt as prompt
import im.env as env




__path_regex = re.compile("""
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

class status(object):
    org_path = None
    dir_path = None
    rel_path = None
    dir_exists = False
    basename = ''


def get_match_names(path_dir, basename):
    "get the file name and dir name at the path_dir. "
    "if basename, filter by the basename"
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
    """ 路径缩写补全: /u/l/b ===> /usr/local/bin """
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
        fan = [] # current path dir list
        for f in fa:
            rel = get_match_names(f, abb)
            for r in rel:
                fan.append(os.path.join(f, r))
        fa = fan
    return fan

@prompt.prompt("path")
def path():
    match = __path_regex.search(env.before)
    if not match:
        return

    status.org_path = match.group()
    status.rel_path = os.path.expanduser(status.org_path)
    status.dir_path = os.path.dirname(status.rel_path)
    status.dir_exists = os.path.exists(status.dir_path)
    status.basename = os.path.basename(status.org_path)

    if status.dir_exists:
        return len(status.basename)
    else:
        return len(status.org_path)


@path
def base(base):
    if status.dir_exists:
        names = get_match_names(status.dir_path, status.basename)
        prompt.append_list(names)
    else:
        paths = try_abbreviation(status.org_path)
        prompt.append_list(paths)




if __name__ == "__main__":
    pass
