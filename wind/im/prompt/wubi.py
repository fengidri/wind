# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:49:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import urllib2
import json

import pyvim
from pyvim import log

import im.env as env
import im.prompt as prompt
import vim

cache={  }

def webget(path):
    r = urllib2.urlopen("http://127.0.0.1:9480%s" % path)
    return json.loads(r.read())

def search_from_db(patten):
    try:
        w = webget("/wubi/search?patten=%s" % patten)
        cache[patten] = w
        return w
    except Exception, e:
        pyvim.echoline(str(e))
        return ([], [])

def search(patten):
    '得到备选的字词'
    words= cache.get( patten )

    if  words:
        return words

    return search_from_db(patten)

def setcount(patten, num):
    w, ass = cache.pop(patten)
    if len(w) -1 < num:
        return
    ww = w[num]
    url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
            ww.encode('utf8'))
    try:
        urllib2.urlopen(url)
    except Exception, e:
        pyvim.echoline(str(e))




@prompt.prompt('wubi')
def handle():
    if not vim.vars.get("wind_im_wubi", 1):
        return

    for i in [-1, -2, -3, -4]:
        try:
            c = env.before[i]
            if not c.islower():
                raise Exception()
        except:
            n = (i + 1) * -1
            if 0 == n:
                return
            return n

    return 4




@handle.base
def wubi(patten):
    log.debug("wubi patten: %s", patten)
    words, associate = search(''.join(patten))

    #abuild(" ", "%s                  " %  patten)

    i = 0
    for w in words:
        i += 1
        prompt.abuild(w, "%s.%s" % (i, w))

    for w, k, c  in associate:
        i += 1
        prompt.abuild( w, "%s.%s %s"%(i, w, k))



if __name__ == "__main__":
    pass

