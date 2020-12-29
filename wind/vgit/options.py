# -*- coding:utf-8 -*-

from . import popup as gitpopup
from . import commit
from . import output
from . import common
import popup

def __commit_log_append(p, arg):
    p.append("=== option log ====")
    cmsg, chash = arg

    commit.run = p.run

    nid = commit.change(chash, cmsg)
    p.append('')
    p.append("=== new git log ====")
    if not nid:
        p.run('git log -1 --no-color')
    else:
        p.run('git log %s~..HEAD --no-color' % nid)

def _commit_log_append(status, arg):
    if not status:
        return

    popup.PopupRun(__commit_log_append, arg)

def commit_log_append(line, target = None, num = 20):
    output.clean()

    def cb(chash):
        if not chash:
            return

        cmsg = commit.cmsg(chash)
        cmsg = cmsg + line
        popup.PopupDialog(cmsg, _commit_log_append, (cmsg, chash),
                title = 'New Commit Log')


    gitpopup.commit_choose(cb, num, target)


