# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-17 17:00:06
#    email     :   fengidri@yeah.net
#    version   :   2.0.1

import pyvim
import vim
import json
import urllib
import urllib2
import tempfile
from textohtml import html
from pyvim import log as logging
import requests

import frainui


#SERVER="shell.fengidri.me"
SERVER = "127.0.0.1:8001"
TEXLIST = None

################################################################################
# 连接服务器
################################################################################
class Remote(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Remote, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if hasattr(self, "map_id_tmp_file"):
            return
        self.map_id_tmp_file = {}

    def file_to_id(self, f):
        for ID, _f in self.map_id_tmp_file.items():
            if _f == f:
                return ID

    def load_list(self):
        URL = "http://%s/store/index.json"%(SERVER)
        #URL = "http://shell.fengidri.me/store/index.json"
        try:
            response = urllib2.urlopen(URL)
            info = response.read()
            info = json.loads(info)
        except:
            pyvim.echo("load index.json fail!")
            info = {}

        for v in info.values():
            if not v.get('title'):
                v['title'] = 'undefined'

            if not v.get('post'):
                v['post'] = '1'

        self.info = info

    def iter(self):
        keys = [int(k) for k in self.info.keys()]
        keys.sort()
        keys.reverse()
        for k in keys:
            yield k, self.info[str(k)]


    def load_tex(self, ID):
        tmp = self.map_id_tmp_file.get(ID)
        if tmp:
            return tmp

        url = 'http://%s/store/%s/index.md' % (SERVER, ID)
        req = urllib2.Request(url)
        tmp = tempfile.mktemp(suffix='.md', prefix='shell_%s_' % ID)
        try:
            res = urllib2.urlopen(req).read()
        except Exception, e:
            pyvim.echo(e)
            return
        open(tmp, 'wb').write(res)
        self.map_id_tmp_file[ID] = tmp
        return tmp

    def post_tex(self, tex, ID):
        j = { 'tex': tex }
        if ID:
            method = "PUT"
            uri = 'http://%s/blog/chapters/%s' % (SERVER, ID)
        else:
            method = "POST"
            uri = 'http://%s/blog/chapters/' % SERVER

        headers = {'Content-Type': "application/json"};
        logging.info("url:%s"%uri)

        res = requests.request(method, uri, headers=headers, data=json.dumps(j))
        return int(res.text)







################################################################################
# 处理 frainui
################################################################################

def add_new(node):
    tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_')
    vim.command('e %s' % tmp)
    vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
    vim.current.buffer.append('%Post:1', 0)
    vim.current.buffer.append('%Class:', 0)
    vim.current.buffer.append('%Title:', 0)
    vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
    return

def leaf_handle(leaf):
    remote = Remote()
    tmp = remote.load_tex(leaf.ctx)
    if not tmp:
        return
    vim.command("edit %s" % tmp)

def list_tex(node):
    remote = Remote()
    remote.load_list()
    for ID, info in remote.iter():
        if node.ctx == "TexList" and info.get("post") != '0':
            name = info.get("title")
            leaf = frainui.Leaf(name, int(ID), leaf_handle)
            node.append(leaf)

        if node.ctx == "UnPost" and info.get("post") == '0':
            name = info.get("title")
            leaf = frainui.Leaf(name, int(ID), leaf_handle)
            node.append(leaf)

def GetRoots(node):
    leaf = frainui.Leaf("NewWiki", -1, add_new)
    node.append(leaf)

    n = frainui.Node("TexList", "TexList", list_tex)
    node.append(n)

    n = frainui.Node("UnPost", "UnPost", list_tex)
    node.append(n)


def GetNames(listwin):
    remote = Remote()
    ID = remote.file_to_id(vim.current.buffer.name)
    if not ID:
        return
    info = remote.info.get(str(ID))
    if not info:
        return
    if info.get('post', '1') == '0':
        names = ['UnPost', info.get('title')]
    else:
        names = ['TexList', info.get('title')]
    logging.error(names)
    listwin.setnames(names)


def ReFreshPre(listwin):
    listwin.Title = "TexList"


################################################################################
# command && event
################################################################################
@pyvim.cmd()
def TexList():
    global  TEXLIST
    TEXLIST = frainui.LIST(GetRoots)

    TEXLIST.FREventBind("ListNames", GetNames)
    TEXLIST.FREventBind("ListReFreshPre", ReFreshPre)
    TEXLIST.show()
    TEXLIST.refresh()



@pyvim.cmd()
def WikiPost():
    if not TEXLIST: return

    remote = Remote()

    ID = remote.file_to_id(vim.current.buffer.name)
    ID = remote.post_tex('\n'.join(vim.current.buffer), ID)

    if ID < 0:
        pyvim.echo("POST error: %d" % ID)
        return

    remote.map_id_tmp_file[ID] = vim.current.buffer.name
    TEXLIST.refresh()

@pyvim.event("CursorHold", "*.mkiv")
@pyvim.event("CursorHoldI", "*.mkiv")
def SendBuf():
    ShowUrl = 'http://localhost/texshow/data'
    data = urllib.urlencode(
            {   "data": '\n'.join(vim.current.buffer),
                "type": "mkiv"})

    req = urllib2.Request(ShowUrl, data)
    try:
        urllib2.urlopen(req).read()
    except Exception, e:
        logging.error(e)

