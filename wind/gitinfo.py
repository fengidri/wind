# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-09 12:05:15
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os

def gitinfo(path):
    cmd = "LANG=en_US git -C %s status --porcelain --branch 2>/dev/null" % path
    lines = os.popen(cmd).readlines()
    if not lines:
        return

    branch='master'
    remote=''

    for line in lines:
        if not line.startswith('##'):
            continue

        t = line.split()
        branch = t[1].split('...')[0]

        if len(branch) > 20:
            if branch.startswith('feature/'):
                branch = branch.split('/')[1]
            branch = branch[-20:]

        if len(t) == 4:
            s = t[2][1:]
            n = t[3][0:-1]
            remote = ' -%s'
            if s == 'ahead':
                remote = ' +%s'
            remote = remote % n

        return {"branch": branch, "remote": remote}


if __name__ == "__main__":
    pass

