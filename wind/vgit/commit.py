# -*- coding:utf-8 -*-
import os
import time

from . import output
from . import common

run = common.run

def amend(msg, log='/dev/null'):
    if msg:
        f = '/tmp/tmp-kernel-patch-%s-%s'  % (time.time(), os.getpid())
        open(f, 'w').write(msg)

        cmd = 'git commit --amend -F %s '% (f, )
        run(cmd)
    else:
        cmd='git commit --amend >>' + log
        run(cmd)



def change(chash, msg = None, log='/dev/null'):
    current_hash = hashs(1)[0]
    if current_hash.startswith(chash):
        amend(msg, log)
        return

    branch = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()


    m = ">> current branch: %s. goto commit %s. change it." % (branch, chash)
    output.buf.append(m)

    cmd='git checkout %s 2>>%s' % (chash, log)
    run(cmd)

    amend(msg, log)

    cmd='git log --pretty=format:%H -1'
    new_commit_id = os.popen(cmd).read().strip()


    m = ">> new commit hash: %s. goto back to branch %s, rebase it.\n" % (new_commit_id, branch)
    output.buf.append(m)

    cmd='git checkout %s 2>>%s' % (branch, log)
    run(cmd)

    cmd='git rebase %s >> %s' % (new_commit_id, log)
    run(cmd)

    return new_commit_id


def hashs(num):
    cmd='git log --pretty=format:%H -' + str(num)
    lines = os.popen(cmd).readlines()
    o = []
    for line in lines:
        o.append(line.strip())
    return o

def cmsg(chash):
    return os.popen('git log --pretty=format:%B -1 ' + chash).read()
