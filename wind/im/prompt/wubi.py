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
import rc

cache={  }

def search_from_db(patten):
    try:
        r = urllib2.urlopen("http://localhost/wubi/search?patten=%s" %
            patten)
        w = json.loads(r.read())
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
    if not rc.IM_Wubi:
        return

    l = len(env.before)
    if l == 0:
        return

    l = min(len(env.before), 4)

    if not env.before[-1].islower():
        return

    if not env.before[-2].islower():
        return 1

    if not env.before[-3].islower():
        return 2

    if not env.before[-4].islower():
        return 3

    return 4



@handle
def wubi(patten):
    log.error("wubi patten: %s", patten)
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

