# -*- coding:utf-8 -*-
import os
import sys
import subprocess
import threading




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

    prefix = '%s\t' % tag

    o = []
    for line in open(tags).readlines():
        if line.startswith(prefix):
            o.append(line.strip())
            continue

    if not o:
        return None, '404 NOT FOUND: %s' % tag

    return o, None

def refresh(root):
    d = os.path.join(root, '.wind_ctags')
    if not os.path.exists(d):
        os.mkdir(d)

    f = os.path.join(d, 'tags')

    os.system("cd %s;ctags --sort=no -f .wind_ctags/tags -R * 2>/dev/null"  % root)

    fd_map = {}

    for line in open(f).readlines():
        p = line[0]
        if '!' == p:
            continue

        fd = fd_map.get(p)
        if not fd:
            fd = open(os.path.join(d, '%s_tags' % p), 'w')
            fd_map[p] = fd

        fd.write(line)


def walk(root,  relat_path = None):
    for item in os.listdir(root):
        if item[0] == '.':
            continue

        full_path = os.path.join(root, item)
        if relat_path:
            relat = os.path.join(relat_path, item)
        else:
            relat = item

        if os.path.isfile(full_path):
            yield relat
        else:
            for item in walk(full_path, relat):
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
    f = os.path.join(f, 'libtag_proc.py')

    cmd = ['python', f, root]

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



if __name__== "__main__":
    #print find_tag(sys.argv[1], sys.argv[2])
    refresh(sys.argv[1])

































