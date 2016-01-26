# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-09 11:44:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from frainui import LIST
import frainui
import libpath
import vim
import pyvim
import utils
import os
from pyvim import log

from project import Project
from white_black import black_filter_files, sorted_by_expand_name

BufNewFile = {}


def leaf_handle(leaf):
    log.debug('leaf_handle: %s', leaf.ctx)
    vim.command( "update")
    path = libpath.pull(leaf.ctx)
    if not path:
        return
    vim.command( "e %s" % path )

def get_child(Node):
    path = Node.ctx
    log.debug("get child path: %s", path)

    dirs, names = libpath.listdir(path)
    if dirs == None:
        return []

    ######## handle for new file
    dels = []
    for f in BufNewFile.get(path, []):
        if f in names:
            dels.append(f)
            continue
        names.append(f)
    if dels:
        for f in dels:
            BufNewFile.get(path).remove(f)


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

def FrainListShowHook(listwin):
    def vimleave():
        Project.emit("FrainLeave")
        if frain.origin_window_title:
            pyvim.settitle(frain.origin_window_title)

    def quitpre():
        return
        ws = vim.windows
        if len(ws) == 2 and listwin.BFw.valid:
            listwin.BFWipeout()

    pyvim.addevent('BufWritePost', libpath.push)
    pyvim.addevent('VimLeave',  vimleave)
    pyvim.addevent("QuitPre", quitpre)

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






################################################################################

class Events(object):
    def del_root_handle(self, node):
        for p in Project.All:
            if p.root == node.ctx:
                p.close()
                self.listwin.refresh()

    def FrainListGetRootsHook(self, node):
        pyvim.Roots = []  # 整个vim 可用的变量

        if vim.vars.get("frain_buffer", 0) == 1:
            dp = r"\green;Buffers\end;"
            root = frainui.Node("Buffers", None, get_buffers, dp)
            self.buf_node = root
            node.append(root)

        for p in Project.All:
            pyvim.Roots.append(p.root)
            root = frainui.Node(p.name, p.root, get_child)
            root.FREventBind("delete", self.del_root_handle)

            node.append(root)

class FrainList(Events):
    def __init__(self):
        self.buf_node = None

        frain.origin_window_title = pyvim.gettitle()

        self.listwin = LIST("frain", self.FrainListGetRootsHook)
        self.listwin.FREventBind("List-ReFresh-Post", FrainListRefreshHook)
        self.listwin.FREventBind("List-ReFresh-Pre",  FrainListRefreshPreHook)
        self.listwin.FREventBind("List-Show",        FrainListShowHook)

        self.listwin.show()
        pyvim.addevent("BufEnter",   self.find)
        pyvim.addevent("BufNewFile", self.bufnewfile)
        pyvim.addevent("BufNew",     self.bufnew)

    def bufnew(self):
        if self.buf_node:
            self.buf_node.refresh()

    def bufnewfile(self):
        path = vim.current.buffer.name
        log.error("bufnewfile buttype: %s.", vim.current.buffer.options['buftype'])
        if vim.current.buffer.options['buftype'] != '':
            return
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        if BufNewFile.get(dirname):
            BufNewFile.get(dirname).append(basename)
        else:
            BufNewFile[dirname] = [basename]

    def find(self):
        if vim.current.buffer.options[ 'buftype' ] != '':
            return -1

        if vim.current.buffer.name == '':
            return -1

        """显示当前的 buffer 对应的文件在 win list 中的位置
        如果, buffer 不属于任何一个 project, 返回 `NROOT'
        之后生成当前 buffer 在 win list 中的 url, 由 win list 进行查询.
        """
        path = utils.bufferpath()
        if not path:
            return
        log.info('path: %s', path)

        for p in Project.All:
            if path.startswith(p.root):
                break
        else:
            return

        names = utils.getnames(p.root, path)
        self.listwin.find(names)

    def add(self, path, name = ''):
        "增加一个新的 project, 提供参数 path, name"
        path = libpath.realpath(path)
        if not path:
            return
        if not name:
            name = libpath.basename(path)

        if path:#TODO maybe scp
            Project(path, name)

        self.listwin.refresh()

    #def add_cur_path(self):
    #    path = utils.bufferpath()
    #    self.add(path, '')

    #def cur_project(self):
    #    "返回当前 bufferf 所有在 project 对象"
    #    path = utils.bufferpath()
    #    for p in Project.All:
    #        if path.startswith(p.root):
    #            return p


class frain(object):
    origin_window_title = None

if __name__ == "__main__":
    pass

