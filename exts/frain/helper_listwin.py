# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-01-26 08:42:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import vim
import pyvim
from pyvim import log

from white_black import black_filter_files, sorted_by_expand_name

import frainui
import libpath

from project import Project

def leaf_handle(leaf, listwin):
    log.debug('leaf_handle: %s', leaf.ctx)
    vim.command("update")

    path = libpath.pull(leaf.ctx)
    if not path:
        return

    vim.command( "e %s" % path )

def get_child(Node, listwin):
    path = Node.ctx
    log.debug("get child path: %s", path)

    dirs, names = libpath.listdir(path)
    if dirs == None:
        return []

    new_files = listwin.frain.new_files
    ######## handle for new file
    dels = []
    for f in new_files.get(path, []):
        if f in names:
            dels.append(f)
            continue
        names.append(f)

    if dels:
        for f in dels:
            new_files.get(path).remove(f)


    names = black_filter_files(names)
    names = sorted_by_expand_name(names)

    dirs  = sorted(black_filter_files(dirs))

    for n in names:
        p = libpath.join(path, n)
        l = frainui.Leaf(n, p, leaf_handle)
        Node.append(l)

    for d in dirs:
        p = libpath.join(path, d)
        Node.append(frainui.Node(d, p, get_child))



def del_root_handle(node, listwin):
    for p in Project.All:
        if p.root == node.ctx:
            p.close()
            listwin.refresh()

def get_buffers(Node):
    names = []
    for b in vim.buffers:
        p = b.name
        if not p:
            continue

        if b.options['buftype'] != '':
            continue

        names.append(p)
    names.sort()

    for p in names:
        Node.append(frainui.Leaf(libpath.basename(p), p, leaf_handle))

    Node.need_fresh = True

def FrainListGetRootsHook(node, listwin):
    pyvim.Roots = []  # 整个vim 可用的变量

    if vim.vars.get("frain_buffer", 0) == 1: # show buffers in listwin
        dp = r"\green;Buffers\end;"
        root = frainui.Node("Buffers", None, get_buffers, dp)
        listwin.frain.buf_node = root
        node.append(root)

    for p in Project.All:
        pyvim.Roots.append(p.root)

        root = frainui.Node(p.name, p.root, get_child)
        root.FREventBind("delete", del_root_handle)

        node.append(root)

################################################################################



def FrainListRefreshHook(listwin):
    if listwin.nu_refresh == 0:
        listwin.first_fresh = False
        Project.emit("FrainEntry")
        return

def FrainListRefreshPreHook(listwin):
    if Project.All:
        p = Project.All[0]
        gitinfo = p.gitinfo
        if not gitinfo:
            title = p.name
        else:
            title = "%s(%s)" % (p.name, gitinfo["branch"])
    else:
        title = 'Frain'

    pyvim.settitle(title)

