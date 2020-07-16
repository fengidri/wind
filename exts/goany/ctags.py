# -*- coding:utf-8 -*-

import os
import sys
import subprocess
import copy

cmd = ['ctags', '--sort=no', '-L', '-', '-f','/dev/null']
cmd = ['ctags', '--sort=no',
        '--c-kinds=+p', '--output-format=xref',
        r"--regex-c=/^SYSCALL_DEFINE[[:digit:]]?\(([^,)]+).*/syscall_\1/",
        r"--regex-asm=/^SYM_CODE_START\(([^,)]+).*/\1/",
        r"--regex-asm=/^SYM_FUNC_START\(([^,)]+).*/\1/",
        r"--regex-asm=/^SYM_INNER_LABEL\(([^,)]+).*/\1/",
        r"--regex-asm=/^ENTRY\(([^,)]+).*/\1/",
        ]

def write_to_tags(d, r):
    fd_map = {}

    i = 0
    left = None

    while True:
        buf = r.read(65422)

        if '' == buf:
            break


        last = 0
        for i,c in enumerate(buf):
            if c != '\n':
                continue

            if last == 0 and left:
                line = left + buf[0:i + 1]
                left = None
            else:
                line = buf[last:i+1]

            last = i + 1


            f = line[0]
            if not f.isalpha() and f != '_':
                continue

            fdb = fd_map.get(f)
            if not fdb:
                path = os.path.join(d, '%s_tags' % f)
                fd = os.open(path, os.O_APPEND|os.O_WRONLY|os.O_CREAT)
                fdb = fd_map[f] = (fd, [])

            fd, b = fdb
            i += 1

            b.append(line)
            if len(b) < 100:
                continue

            os.write(fd, ''.join(b))
            del b[:]

        if buf[-1] != '\n':
            last = buf[i:]

    for fd, b in fd_map.values():
        os.write(fd, ''.join(b))



def main():
    root = sys.argv[1]
    os.chdir(root)

    cmd.append('--filter=yes')

    p = subprocess.Popen(cmd, stdin=sys.stdin, stdout=subprocess.PIPE, universal_newlines=True)
    d = os.path.join(root, '.wind_ctags')
    write_to_tags(d, p.stdout)
    p.wait()

def parse(path):
    c = copy.copy(cmd)
    c.append('-f')
    c.append('-')
    c.append(path)
    p = subprocess.Popen(c, stdout=subprocess.PIPE, universal_newlines=True)
    lines = p.stdout.readlines()
    p.wait()
    return lines

if __name__== "__main__":
    main()

