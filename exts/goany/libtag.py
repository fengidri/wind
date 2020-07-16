# -*- coding:utf-8 -*-
import os
import sys
import subprocess
import threading
import ctags

class g:
    iskernel = False

# d  macro definitions
# e  enumerators (values inside an enumeration)
# f  function definitions
# g  enumeration names
# h  included header files
# l  local variables [off]
# m  struct, and union members
# p  function prototypes [off]
# s  structure names
# t  typedefs
# u  union names
# v  variable definitions
# x  external and forward variable declarations [off]
# z  function parameters inside function definitions [off]
# L  goto labels [off]
# D  parameters inside macro definitions [off]

class Line(object):
    def __init__(self, line):
        self.show = None
        self.pattern = None

        if ';"' in line:
            t = line.split('\t', 2)

            self.tag = t[0]
            self.file_path = t[1]

            pos = t[2].find(';"\t')

            pattern = t[2][0:pos]

            if pattern.isdigit():
                pattern = int(pattern) - 1
                self.line_nu = pattern
            else:
                pattern = pattern[2:-2]
                pattern = pattern.replace('\\t', '\t').replace('\\/', '/')
                pattern = pattern.replace(r'\r','')
                #pattern = encode(pattern)
            self.pattern = pattern

            t = t[2][pos:].split('\t')

            kind_map = {'p':'prototype',
                    'f': 'function',
                    'm': 'member',
                    's': 'struct',
                    'v': 'variable',
                    'd': 'marco',
                    'e': 'enumerator',
                    }
            self.kind = kind_map.get(t[1], self.kind)

        else: # xref
            t = line.split(None, 4)
            self.tag = t[0]
            self.kind = t[1]
            self.file_path = t[3]
            self.line_nu = int(t[2]) - 1
            self.show = t[4]

def tag_file(root, tag):
    p = os.path.join(root, '.wind_ctags/%s_tags' % tag[0])
    if os.path.isfile(p):
        return p

    p = os.path.join(root, '.tags')
    if os.path.isfile(p):
        return p

    p = os.path.join(root, 'tags')
    if os.path.isfile(p):
        return p


def find_tag(root, tag):
    tags = tag_file(root, tag)
    if not tags:
        return  None, 'not found tags/.ctags at %s' % tags

    prefix = '%s ' % tag

    o = []
    for line in open(tags).readlines():
        if line.startswith(prefix):
            o.append(line.strip())
            continue

    if not o:
        return None, '404 NOT FOUND: %s' % tag

    return o, None


def walk(root,  relat_path = None, depth=0):
    for item in os.listdir(root):
        if item[0] == '.':
            continue

        if 0 == depth:
            if item == 'tools' or item == 'samples' or item == 'scripts':
                continue

        full_path = os.path.join(root, item)
        if relat_path:
            relat = os.path.join(relat_path, item)
        else:
            relat = item

        if os.path.isfile(full_path):
            yield relat

        if os.path.isdir(full_path):
            for item in walk(full_path, relat, depth + 1):
                yield item



def send_stdin(root, ps):
    i  = 0

    for path in walk(root):
        path = path + '\n'
        p = ps[i % len(ps)]
        p.stdin.write(path)
        i += 1

    for p in ps:
        p.stdin.close()

    return i

def ctags_proc(num, root):
    ps = []
    i = 0
    f = os.path.realpath(__file__)
    f = os.path.dirname(f)
    f = os.path.join(f, 'ctags.py')

    cmd = ['python2', f, root]

    while i < num:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, universal_newlines=True)

        ps.append(p)
        i += 1

    return ps



def refresh(root):
    d = os.path.join(root, '.wind_ctags')
    if not os.path.exists(d):
        os.mkdir(d)

    for item in os.listdir(d):
        path = os.path.join(d, item)
        open(path, 'w').close()


    ps = ctags_proc(50, root)

    send_stdin(root, ps)

    for p in ps:
        p.wait()

def parse(path):
    o = []

    for line in ctags.parse(path):
        o.append(Line(line))

    return o




if __name__== "__main__":
    #print find_tag(sys.argv[1], sys.argv[2])
    refresh(sys.argv[1])

































