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

import frainui

ID = None
SERVER="blog.fengidri.me"
is_wiki = False

map_id_file = {}
map_file_leaf = {}

TEXLIST = None
TEXINFO = None

def load_list():
    URL = "http://blog.fengidri.me/store/index.json"
    try:
        response = urllib2.urlopen(URL)
        info = response.read()
        info = json.loads(info)
        info.reverse()
        return info
    except:
        pyvim.echo("load index.json fail!")
        return []

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

def leaf_handle(leaf):
    tmp = load_tex(leaf.ctx)
    if not tmp:
        return
    map_file_leaf[tmp] = leaf
    vim.command("edit %s" % tmp)

def GetRoots(node):
    for info in load_list():
        name = info[1]
        ID = info[0]
        leaf = frainui.Leaf(name, ID, leaf_handle)
        node.append(leaf)

def GetNames(listwin):
    leaf = map_file_leaf.get(vim.current.buffer.name)
    if not leaf:
        return
    listwin.setnames([leaf.name])




@pyvim.cmd()
def WikiList():
    global  TEXLIST
    TEXLIST = frainui.LIST(GetRoots)
    TEXLIST.FREventBind("ListNames", GetNames)
    TEXLIST.refresh()



@pyvim.cmd()
def WikiPost():
        if not is_wiki:
            return
        info, c = content()

        global ID
        if ID:
            pyvim.echoline('ID:%s, You should run WikiPut.' % ID)
            return

        ID = post(c, info)
        ID = int(ID)
        pyvim.echoline('ID:%s' % ID)

@pyvim.cmd()
def WikiPut():
        if not is_wiki:
            return
        global ID
        if ID == None:
            pyvim.echoline('ID:None, You should run WikiPost.')
            return

        try:
            info, c = content()
        except:
            return

        ID =  put( c, info)
        ID = int(ID)
        pyvim.echoline('ID:%s' % ID)

@pyvim.cmd()
def WikiGet(_ID):
        global ID
        global is_wiki
        is_wiki = True
        tmp = get(_ID)
        if not tmp:
            return
        ID = _ID
        vim.command("edit %s" % tmp)

@pyvim.cmd()
def WikiNew():
        global is_wiki
        is_wiki = True
        tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_')
        vim.command('e %s' % tmp)
        vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)
        vim.current.buffer.append('%Post:1', 0)
        vim.current.buffer.append('%Class:', 0)
        vim.current.buffer.append('%Title:', 0)
        vim.current.buffer.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', 0)


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

def get(ID):
    url = 'http://%s/store/%s/index.mkiv' % (SERVER, ID)
    req = urllib2.Request(url)
    tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_%s_' % ID)
    try:
        res = urllib2.urlopen(req).read()
    except Exception, e:
        print e
        return
    open(tmp, 'wb').write(res)
    return tmp



def post(tex, info):
    j = {
            'title':info.get('title'),
            'tex': tex,
            'html': html(buf = tex),
            'class': info.get('class', ''),
            'post': info.get('post', 'true')
            }

    url = 'http://%s/fwikiapi/chapters' % SERVER
    req = urllib2.Request(url, json.dumps(j));
    req.add_header('Content-Type', "application/json");
    return urllib2.urlopen(req).read()

def put(tex, info):
    if not ID:
        return
    logging.error('put')
    j = {
            'title':info.get('title'),
            'tex': tex,
            'html': html(buf = tex),
            'class': info.get('class', ''),
            'post': info.get('post', '1')
            }
    url = 'http://%s/fwikiapi/chapters/%s' % (SERVER, ID)

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, json.dumps(j));
    logging.error('put1')

    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'PUT'
    return opener.open(request).read().strip()




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

