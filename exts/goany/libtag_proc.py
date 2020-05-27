# -*- coding:utf-8 -*-

import os
import sys
import subprocess

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

            fd = fd_map.get(f)
            if not fd:
                path = os.path.join(d, '%s_tags' % f)
                fd = os.open(path, os.O_APPEND|os.O_WRONLY|os.O_CREAT)
                fd_map[f] = fd

            i += 1
            os.write(fd, line)
        if buf[-1] != '\n':
            last = buf[i:]


root = sys.argv[1]
os.chdir(root)
cmd = ['ctags', '--sort=no', '-L', '-', '-f','/dev/null']
cmd = ['ctags', '--sort=no', '--filter=yes',
        '--c-kinds=+p',
        r"--regex-c=/^SYSCALL_DEFINE[[:digit:]]?\(([^,)]+).*/\1/"]
p = subprocess.Popen(cmd, stdin=sys.stdin, stdout=subprocess.PIPE, universal_newlines=True)
d = os.path.join(root, '.wind_ctags')
write_to_tags(d, p.stdout)
p.wait()
