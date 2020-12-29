# -*- coding:utf-8 -*-

from . import popup as gitpopup
from . import commit
from . import output
from . import common
import popup

def _commit_log_append(status, arg):
    if not status:
        return

    cmsg, chash = arg
    nid = commit.change(chash, cmsg)

    if not nid:
        common.run('git log -1 --no-color')
    else:
        common.run('git log %s..HEAD --no-color' % nid)

    popup.PopupDialog(output.buf, title = 'git option log')

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


