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
        return -3

    l = len(env.before)
    l = min(l, 4)
    index = -1
    while l > 0:
        if not env.before[index].islower():
            break
        index -= 1
        l -= 1
    if index == -1:
        raise prompt.NotPrompt()
    col = env.col - index * -1  + 1
    return col

@handle
def wubi(patten):
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

