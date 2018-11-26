# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-26 11:04:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import urllib2
import json

import pyvim
from pyvim import log

import im.env as env
import im.prompt as prompt
import vim

import im.keybase
import pyvim

import vim
from im import imrc
feedkeys = imrc.feedkeys

class IM_Wubi_Pum(im.keybase.BaseEnd):
    def cb_tab(self):
        feedkeys('\<C-n>')
        return True


    def cb_esc(self):
        feedkeys('\<esc>')
        return True

    def cb_enter(self):
        feedkeys('\<C-e>')
        return True

    def cb_space(self):
        feedkeys('\<C-N>')
        feedkeys('\<C-Y>')
        return True

    def cb_backspace(self):
        feedkeys('\<bs>')
        #feedkeys('\<C-X>\<C-O>\<C-P>')  # TODO   should auto
        return True

    def im_lower(self, k):
        # call wubi

        func = "wind#Prompt"

        vim.command("let &omnifunc='%s'" % func)
        vim.command("let &l:omnifunc='%s'" % func)

        imrc.feedkeys('\<C-Y>')
        imrc.feedkeys(k)
        imrc.feedkeys('\<C-X>\<C-O>')
        return True

    def handler(self, tp, key):
        getattr(self, tp)(key)


im_wub_pumvisible_handler =  IM_Wubi_Pum()

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




def findstart():
    log.error("#########: %s", env.before)
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

def base(patten):
    log.debug("wubi patten: %s", patten)
    words, associate = search(''.join(patten))

    #abuild(" ", "%s                  " %  patten)

    env.pumvisible_handler = im_wub_pumvisible_handler.handler

    i = 0
    for w in words:
        i += 1
        prompt.abuild(w, "%s.%s" % (i, w))

    for w, k, c  in associate:
        i += 1
        prompt.abuild( w, "%s.%s %s"%(i, w, k))



class IM_Wubi(im.keybase.BaseEnd):
    def isenable(self):
        if not vim.vars.get("wind_im_wubi", 1):
            return

    def im_lower(self, k):
        if not self.isenable():
            imrc.feedkeys(k)
            return


        func = "wind#Prompt"

        vim.command("let &omnifunc='%s'" % func)
        vim.command("let &l:omnifunc='%s'" % func)

        prompt.findstart = findstart
        prompt.base = base

        imrc.feedkeys(k)
        imrc.feedkeys('\<C-X>\<C-O>')
        return True

    def handler(self, tp, key):
        getattr(self, tp)(key)




