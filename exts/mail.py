# -*- coding:utf-8 -*-
import pyvim
import fm
import vim

from frainui import LIST
import frainui
from pyvim import log as logging
import time

class g:
    default = None

def leaf_handle(leaf, listwin):
    mail = leaf.ctx

    vim.command('r  ' + mail.path)
    vim.command("setlocal nomodifiable")
    vim.command("set filetype=fmpager")


def get_child(node, listwin):
    mbox = fm.Mbox(fm.conf.mbox[0])

    ms = mbox.output(reverse=True)


    fmt = '{stat} {subject} {_from} {date}'

    head = None
    for m in ms:
        if head != m.thread_head:
            if head:
                l = frainui.Leaf('', None, leaf_handle)
                node.append(l)

            head = m.thread_head

        if m.isnew:
            stat = '*'
        else:
            stat = ' '

        date = m.Date_ts()
        date = time.strftime("%m-%d %H:%M", time.localtime(date))

        subject = '%s %s' % (m.thread_prefix(), m.Subject())
        subject = subject.ljust(80)[0:80]

        f = m.From()
        f = fm.EmailAddr(f)
        f = f.short
        if f != '':
            f = 'From: %s' % f

        f = f.ljust(20)[0:20]

        s = fmt.format(stat = stat,
                       subject = subject,
                       _from = f,
                       date = date);

        l = frainui.Leaf(s, m, leaf_handle)
        node.append(l)


def list_root(node, listwin):
    r = frainui.Node("FM.feng mail", None, get_child)
    node.append(r)

    if g.default == None:
        g.default = r




@pyvim.cmd()
def Mail():
    b = vim.current.buffer
    if len(b) != 1:
        return

    if not fm.conf.mbox:
        return

    mbox = fm.Mbox(fm.conf.mbox[0])


    listwin = LIST("frain", list_root, ft='fmindex',
            use_current_buffer = True)
    listwin.show()
    listwin.refresh()
    g.default.node_open()



