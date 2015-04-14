# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-17 17:00:06
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import pyvim
import vim
import json
import urllib2
import tempfile
from textohtml import texstohtmls
ID = None
SERVER="blog.fengidri.me"
class WikiPost(pyvim.command):
    def run(self):
        info, c = content()

        global ID
        if ID:
            pyvim.echoline('ID:%s, You should run WikiPut.' % ID)
            return

        ID = post(c, info)
        ID = int(ID)
        pyvim.echoline('ID:%s' % ID)

class WikiPut(pyvim.command):
    def run(self):
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

class WikiGet(pyvim.command):
    def run(self):
        global ID
        if not self.params:
            print "should input the ID of the cachpter"
            return
        _ID = self.params[0]
        tmp = get(_ID)
        if not tmp:
            return
        ID = _ID
        vim.command("edit %s" % tmp)
class WikiNew(pyvim.command):
    def run(self):
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
            'html': texstohtmls(tex),
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
    j = {
            'title':info.get('title'),
            'tex': tex,
            'html': texstohtmls(tex),
            'class': info.get('class', ''),
            'post': info.get('post', '1')
            }
    url = 'http://%s/fwikiapi/chapters/%s' % (SERVER, ID)

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, json.dumps(j));

    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'PUT'
    return opener.open(request).read().strip()













