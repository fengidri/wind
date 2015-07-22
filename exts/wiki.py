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

ID = None
SERVER="blog.fengidri.me"
is_wiki = False

map_id_file = {}
map_file_leaf = {}


TEXLIST = None
class Cfg(object):
    texlist = None
    texinfo = None

    @classmethod
    def get_name_by_id(cls, ID):
        for info in cls.texinfo:
            if info[0] == ID:
                return info[1]

    def get_file_by_id(cls, ID):
        pass


################################################################################
# paser content
################################################################################
def getv(line):
    tmp = line[1:].split(':')
    if len(tmp) < 2:
        return []
    return [tmp[0].strip().lower(), tmp[1].strip()]


def content():
    info = {}
    for line in vim.current.buffer:
        if len(line) < 2 or line[0] != '%':
            if not info.get('title'):
                print "not find title"
                return
            break
        try:
            k,v = getv(line)
            info[k] = v
        except:
            pass

    if not info.get('title'):
        print "not find title"
        return
    content = '\n'.join(vim.current.buffer)
    return (info, content)

################################################################################
# 连接服务器
################################################################################

def load_list():
    URL = "http://blog.fengidri.me/store/index.json"
    try:
        response = urllib2.urlopen(URL)
        info = response.read()
        info = json.loads(info)
        info.reverse()
    except:
        pyvim.echo("load index.json fail!")
        info = []
    Cfg.texinfo = info
    return info

def load_tex(ID):
    tmp = map_id_file.get(ID)
    if tmp:
        return tmp

    url = 'http://%s/store/%s/index.mkiv' % (SERVER, ID)
    req = urllib2.Request(url)
    tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_%s_' % ID)
    try:
        res = urllib2.urlopen(req).read()
    except Exception, e:
        pyvim.echo(e)
        return
    open(tmp, 'wb').write(res)
    map_id_file[ID] = tmp
    return tmp

def post_tex(tex, info, ID):
    j = {
            'title':info.get('title'),
            'tex': tex,
            'html': html(buf = tex),
            'class': info.get('class', ''),
            'post': info.get('post', 'true')
            }
    if ID:
        method = "PUT"
        uri = 'http://%s/fwikiapi/chapters/%s' % (SERVER, ID)
    else:
        method = "POST"
        uri = 'http://%s/fwikiapi/chapters' % SERVER

    headers = {'Content-Type': "application/json"};

    res = requests.request(method, uri, headers=headers, data=json.dumps(j))
    return int(res.text)


################################################################################
# 处理 frainui
################################################################################

def leaf_handle(leaf):
    if -1 == leaf.ctx: # new wiki
        tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_')
        vim.command('e %s' % tmp)
        vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
        vim.current.buffer.append('%Post:1', 0)
        vim.current.buffer.append('%Class:', 0)
        vim.current.buffer.append('%Title:', 0)
        vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
        return

    tmp = load_tex(leaf.ctx)
    if not tmp:
        return
    map_file_leaf[tmp] = (leaf.ctx, leaf.name)
    vim.command("edit %s" % tmp)

def GetRoots(node):
    leaf = frainui.Leaf("new wiki", -1, leaf_handle)
    node.append(leaf)
    for info in load_list():
        name = info[1]
        ID = info[0]
        leaf = frainui.Leaf(name, ID, leaf_handle)
        node.append(leaf)

#def GetNames(listwin):
#    ID, name = map_file_leaf.get(vim.current.buffer.name)
#    if not leaf:
#        return
#    listwin.setnames([name])


def ReFreshPre(listwin):
    listwin.Title = "TexList"


################################################################################
# command && event
################################################################################

@pyvim.cmd()
def TexList():
    global  TEXLIST
    TEXLIST = frainui.LIST(GetRoots)
    #TEXLIST.FREventBind("ListNames", GetNames)
    TEXLIST.FREventBind("ListReFreshPre", ReFreshPre)
    TEXLIST.show()
    TEXLIST.refresh()



@pyvim.cmd()
def WikiPost():
    if not TEXLIST: return

    ID = None
    info, c = content()
    tt = map_file_leaf.get(vim.current.buffer.name)

    if tt:
        need_fresh = False
        ID = tt[0]

    _ID = post_tex(c, info, ID)

    if ID == None:
        map_id_file[_ID] = vim.current.buffer.name
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

