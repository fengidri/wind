# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-17 17:00:06
#    email     :   fengidri@yeah.net
#    version   :   2.0.1

import pyvim
import vim
from pyvim import log as logging
import requests

import frainui
from remote import Remote

import sendbuf

import units

TEXLIST = None







################################################################################
# 处理 frainui
################################################################################

def add_new(node):
    tmp = units.tmpfile()
    vim.command('e %s' % tmp)
    vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
    vim.current.buffer.append('%Post:1', 0)
    vim.current.buffer.append('%Class:', 0)
    vim.current.buffer.append('%Title:', 0)
    vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
    Remote().news.append(tmp)
    TEXLIST.refresh()
    find()
    return

def leaf_handle(leaf):
    remote = Remote()
    tmp = remote.load_tex(leaf.ctx)
    if not tmp:
        return
    vim.command("edit %s" % tmp)

def leaf_delete(leaf):
    if not vim.vars.get('wiki_del_enable'):
        pyvim.echo('Please let g:wiki_del_enable=1', hl=True)
        return
    url = units.URL_PUT % (units.SERVER, leaf.ctx)
    res = requests.request('delete', url)
    leaf.father.refresh()


def list_tex(node):
    remote = Remote()
    remote.load_list()
    for ID_s, info in remote.iter():
        if node.ctx == "TexList" and info.get("post") == '0':
            continue

        if node.ctx == "UnPost" and info.get("post") == '1':
            continue

        name = info.get("title")
        leaf = frainui.Leaf(name, ID_s, leaf_handle)
        leaf.FREventBind("delete", leaf_delete)
        node.append(leaf)


def List1(node):
    Remote().load_list() # 重新更新一下数据

    leaf = frainui.Leaf("NewWiki", -1, add_new, display = "\\red;NewWiki\\end;")
    node.append(leaf)

    for i, new in enumerate(Remote().news):
        name = "undefined:%d" % i
        dp   = "\\blue;%s\\end;" % name
        leaf = frainui.Leaf(name, new, leaf_handle, display = dp)
        node.append(leaf)

    n = frainui.Node("TexList", "TexList", list_tex)
    node.append(n)

    n = frainui.Node("UnPost", "UnPost", list_tex)
    node.append(n)


def find(filename = None):
    if not filename:
        filename = vim.current.buffer.name

    remote = Remote()
    ID_s = remote.get_id_by_name(filename)

    if ID_s == None:
        if filename in remote.news:
            i = remote.news.index(filename)
            TEXLIST.find(["undefined:%d" % i])
    else:
        info = remote.info.get(ID_s)
        if not info:
            return
        if info.get('post', '1') == '0':
            names = ['UnPost', info.get('title')]
        else:
            names = ['TexList', info.get('title')]

        TEXLIST.find(names)



def ReFreshPre(listwin):
    listwin.Title = "TexList"


################################################################################
# command && event
################################################################################
@pyvim.cmd()
def TexList():
    if not (units.SERVER and units.URL_INDEX and units.URL_CHAPTER and units.URL_PUT and units.URL_POST):
        pyvim.echo("Please set config for wiki.", hl=True)
        return

    global  TEXLIST
    if TEXLIST:
        return

    TEXLIST = frainui.LIST("TexList", List1)
    TEXLIST.FREventBind("ListReFreshPre", ReFreshPre)
    TEXLIST.show()
    TEXLIST.refresh()

    pyvim.addevent("BufEnter", find)



@pyvim.cmd()
def WikiPost():
    if not TEXLIST: return

    remote = Remote()
    curfile = vim.current.buffer.name

    ID_i = remote.post_tex('\n'.join(vim.current.buffer), curfile)

    if ID_i == None:
        return

    if ID_i < 0:
        pyvim.echo("POST error: %s" % ID_i, hl=True)
        return

    remote.update(ID_i, curfile)
    TEXLIST.refresh()
    find(curfile)


