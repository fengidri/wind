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
from pyvim import log as logging
import requests

import frainui
from textohtml import html

SERVER      = vim.vars.get("wind_wiki_server")
URL_INDEX   = vim.vars.get("wind_wiki_index")
URL_CHAPTER = vim.vars.get('wind_wiki_chapter')      # 后缀用于临时文件的类型
URL_PUT     = vim.vars.get("wind_wiki_api_chapter")
URL_POST    = vim.vars.get("wind_wiki_api_chapters")

TEXLIST = None


def tmpfile():
    sf = ".%s" % URL_CHAPTER.split('.')[-1]
    return tempfile.mktemp(suffix=sf, prefix='fwiki_')

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
        self.news = []
        self.load_list()

    def get_id_by_name(self, name): # 返回的ID 是str
        if name in self.news:
            return None

        for ID, _f in self.map_id_tmp_file.items():
            if _f == name:
                return str(ID)

    def update(self, ID, name):
        ID = str(ID)
        if name in self.news:
            self.news.remove(name)

        self.map_id_tmp_file[ID] = name


    def load_list(self):
        try:
            response = urllib2.urlopen(URL_INDEX % SERVER)
            info = response.read()
            info = json.loads(info)
        except:
            pyvim.echo("load index.json fail!", hl=True)
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
            yield str(k), self.info[str(k)]


    def load_tex(self, ID_s):
        tmp = self.map_id_tmp_file.get(ID_s)
        if tmp:
            return tmp

        url = URL_CHAPTER % (SERVER, ID_s)
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req).read()
        except Exception, e:
            pyvim.echo(e, hl=True)
            return

        tmp = tmpfile()
        open(tmp, 'wb').write(res)
        self.map_id_tmp_file[ID_s] = tmp
        return tmp

    def post_tex(self, tex, name): # 返回的 ID 是 int
        j = { 'tex': tex }

        if URL_CHAPTER.endswith('.mkiv'):
            j['html'] = html(buf = tex)

        ID = self.get_id_by_name(name)
        if ID:
            method = "PUT"
            uri = URL_PUT % (SERVER, ID)
        else:
            method = "POST"
            uri = URL_POST % SERVER

        headers = {'Content-Type': "application/json"};

        res = requests.request(method, uri, headers=headers, data=json.dumps(j))
        return int(res.text)







################################################################################
# 处理 frainui
################################################################################

def add_new(node):
    tmp = tmpfile()
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
    url = URL_PUT % (SERVER, leaf.ctx)
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

    if ID_i < 0:
        pyvim.echo("POST error: %d" % ID, hl=True)
        return

    remote.update(ID_i, curfile)
    TEXLIST.refresh()
    find(curfile)

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

