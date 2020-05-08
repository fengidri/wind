# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2018-11-26 11:04:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# set g:wind_im_wubi inside ftplugin to open/close wubi


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


cache={  }

def search(patten):
    '得到备选的字词'
    words= cache.get( patten )

    if words:
        return words

    w = wbtree.wbsearch(patten)
    cache[patten] = w
    return w


class g:
    base = None


class IM_Wubi_Pum(prompt.PromptKey):
    def im_lower(self, k):
        # 一些情况下, 连接输入的字符会导致空字符或者说两次输入的字符都没有了
        # 在 tex 文件类型下测试没有问题, 但是在 c 下面测试的时候出现了问题.
        # 增加 <C-E> 明确要求, 回复到之前的状态, 再输入新的字符可以解决这个问题.
        imrc.feedkeys('\<C-Y>')
        imrc.feedkeys(k)
        prompt.active()
        return True

    im_upper = im_lower

    def cb_space(self):
        if g.base and env.before.endswith(g.base):
            imrc.feedkeys('\<C-N>')

        imrc.feedkeys('\<C-Y>')
        return True

    def cb_digit1(self):
        imrc.feedkeys('\<C-N>')
        imrc.feedkeys('\<C-Y>')

    def cb_digit2(self):
        imrc.feedkeys('\<C-N>'*2)
        imrc.feedkeys('\<C-Y>')

    def cb_digit3(self):
        imrc.feedkeys('\<C-N>'*3)
        imrc.feedkeys('\<C-Y>')

    def cb_digit4(self):
        imrc.feedkeys('\<C-N>'*4)
        imrc.feedkeys('\<C-Y>')

    def cb_digit5(self):
        imrc.feedkeys('\<C-N>'*5)
        imrc.feedkeys('\<C-Y>')

    def cb_digit6(self):
        imrc.feedkeys('\<C-N>'*6)
        imrc.feedkeys('\<C-Y>')

    def cb_digit7(self):
        imrc.feedkeys('\<C-N>'*7)
        imrc.feedkeys('\<C-Y>')

    def cb_digit8(self):
        imrc.feedkeys('\<C-N>'*8)
        imrc.feedkeys('\<C-Y>')

    def cb_digit9(self):
        imrc.feedkeys('\<C-N>'*9)
        imrc.feedkeys('\<C-Y>')

class wb_prompt(prompt.Prompt):
    def findstart(self):
        log.debug("wubi patten findstart before: %s", env.before)

        l = len(env.before)
        if l > 4:
            l = 4

        i = 1
        while i <= l:
            ii = i * -1
            i += 1

            c = env.before[ii]

            if not c.islower():
                n = (ii + 1) * -1
                if 0 == n:
                    return
                return n

        return i - 1

    def base(self, patten):

        g.base = patten

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




