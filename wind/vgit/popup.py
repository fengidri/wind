# -*- coding:utf-8 -*-



import popup
from . import log


def commit_choose(cb, num = 20, target = None):
    l = log.log(num)
    o = []
    for sh, title in l:
        o.append(sh + ' ' + title)

    def _f(i):
        if i < 0:
            cb(None)
            return

        cb(l[i][0])

    popup.PopupSelect(o, _f, target = target, title = 'commit choose')
