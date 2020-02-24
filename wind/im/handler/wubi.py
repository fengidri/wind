# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-26 11:04:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# set g:wind_im_wubi inside ftplugin to open/close wubi


import urllib3
import json

import pyvim
from pyvim import log

import im.env as env
import im.prompt as prompt
import vim

import im.keybase
import pyvim
import wbtree

import vim
from im import imrc
feedkeys = imrc.feedkeys

cache={  }

def search(patten):
    '得到备选的字词'
    words= cache.get( patten )

    if words:
        return words

    w = wbtree.wbsearch(patten)
    cache[patten] = w
    return w



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
        #uchar = env.before[-1]
        #if (uchar >= u'u0041' and uchar<=u'u005a') or \
        #        (uchar >= u'u0061' and uchar<=u'u007a'):
        feedkeys('\<C-N>')
        feedkeys('\<C-Y>')
        return True

    def cb_backspace(self):
        feedkeys('\<bs>')
        #feedkeys('\<C-X>\<C-O>\<C-P>')  # TODO   should auto
        return True

    def im_lower(self, k):
        imrc.feedkeys(k)
        prompt.co_active()
        return True



class wb_prompt(prompt.Prompt):
    def findstart(self):
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

    def base(self, patten):
        log.debug("wubi patten: %s", patten)
        words, associate = search(''.join(patten))

        i = 0
        for w in words:
            i += 1
            self.abuild(w, "%s.%s" % (i, w))

        for w, k, c  in associate:
            i += 1
            self.abuild( w, "%s.%s %s"%(i, w, k))


prompt = wb_prompt(IM_Wubi_Pum())

class IM_Wubi(im.keybase.BaseEnd):

    def isenable(self):
        return vim.vars.get("wind_im_wubi", 1)

    def im_lower(self, k):
        if not self.isenable():
            imrc.feedkeys(k)
            return

        imrc.feedkeys(k)

        prompt.active()
        return True




