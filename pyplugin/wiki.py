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
ID = None
SERVER="localhost"
class WikiPost(pyvim.command):
    def run(self):
        title, cls, c = content()

        global ID
        if ID:
            ID =  put(title, c, cls)
        else:
            ID = post(title, c, cls)
        ID = int(ID) 
        print ID

class WikiPut(pyvim.command):
    def run(self):
        global ID
        if not ID:
            print "not ID. Should WikiPost" 
            return 
        try:
            title, cls, c = content()
        except:
            return

        ID =  put(title, c, cls)
        ID = int(ID) 
        print ID

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

def getv(line):
    return line.split(':')[-1].strip()


def content():
        title = ''
        cls = ''
        for line in vim.current.buffer:
            if line.startswith('%%') or len(line) < 2 or line[0] != '%':
                if not title:
                    print "not find title"
                    return
                break


            if line.find('title')>-1:
                title = getv(line)
            elif line.find('class')>-1:
                cls = getv(line)

        if not title:
            print "not find title"
            return
        content = '\n'.join(vim.current.buffer)
        return (title, cls, content)
def get(ID):
    url = 'http://%s/fwiki/chapters/%s' % (SERVER, ID)
    req = urllib2.Request(url)
    req.add_header('Accept', "text/json+mkiv")
    tmp = tempfile.mktemp(suffix='.mkiv', prefix='fwiki_')
    try:
        res = urllib2.urlopen(req).read()
    except Exception, e:
        print e
        return
    c = json.loads(res).get('content')
    if not c:
        print "not content"
        return 
    open(tmp, 'w').write(c.encode('utf8'))
    return tmp



def post(title, content, cls):
    j = {'title':title, 'content': content, 'class': cls}
    url = 'http://%s/fwiki/chapters' % SERVER
    req = urllib2.Request(url, json.dumps(j));

    req.add_header('Content-Type', "application/json");
    return urllib2.urlopen(req).read()

def put(title, content, cls='', tags=[]):
    if not ID:
        return
    j = {'title':title, 'content': content, 'class': cls}
    url = 'http://%s/fwiki/chapters/%s' % (SERVER, ID)

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, json.dumps(j));

    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'PUT'
    return opener.open(request).read().strip()













