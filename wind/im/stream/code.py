# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:57:20
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import re
from im.imrc import feedkeys
import vim

import im.prompt as prompt
from pyvim import log as logging

import im.env  as env
import im.keybase

class handle(object):
    def double_out(self, d, b):
        if env.after == '':
            feedkeys([d , b , '\\<left>'])
        else:
            feedkeys(d)
        return True

    def cb_bracket( self ):#[  ]
        self.double_out('[', ']')
        return True

    def cb_parenthess( self ):#(  )
        self.double_out('(', ')')
        return True

    def out_marks(self, p):
        c = env.before.count(p) + env.after.count(p)
        if c % 2 == 0:
            feedkeys([p , p , '\\<left>'])
        else:
            feedkeys(p)

    def cb_mark( self ):
        self.out_marks("'")
        return True

    def cb_double_mark( self ):
        self.out_marks('"')
        return True

    def cb_tab( self ):
        if re.search(r'^\s*$', env.before):
            o = '    '
            feedkeys(o)
        else:
            self.ycm = True
        return True


    def cb_brace(self):#{  }
        if env.after == '' and  env.before.strip().endswith(')'):
            feedkeys('\<cr>{\<cr>}\<up>\<cr>')
            return True
        self.double_out('{', '}')
        return True

    def cb_dot(self):
        feedkeys('.')
        self.ycm = True
        return True

    def cb_underline(self):
        feedkeys('_')
        return True


    #def cb_backspace(self):
    #    #for c in env.before:
    #    #    if c != ' ':
    #    #        break
    #    #else: #
    #    #    l = len(env.before)
    #    #    if l != 0:
    #    #        left = l % 4
    #    #        if left == 0:
    #    #            left = 4
    #    #        feedkeys('\<bs>' * left)
    #    #        return True

    #    feedkeys('\<bs>')
    #    return True

import im.imrc as imrc
from .. import stream


class ycm_prompt(prompt.Prompt):
    trigger_key = ('\<C-c>', 'm')

prompt = ycm_prompt()


def timer_callback():
    # 目前用于在 cursor hold 的时候触发补全
    # 不使用 CursorHoldI 事件是由于这事件触发时间比较长 4000ms
    # 同时这个时间还用于 swap, 并不方便修改

    s = pyvim.pyvim.str_before_cursor()
    if len(s) < 2:
        return

    if not s[-1].isalpha():
        return

    prompt.active(delay = False)
    #pyvim.feedkeys(('\<C-c>', 'm'))


class IM_Code(im.keybase.BaseEnd, handle):
    wubi_syntax = ['Constant', 'CCommentDesc', 'CCommentArg', 'Comment', 'String']
    fts = ['python', 'javascript', 'ch', 'vim', 'html', 'sh', 'lua']

    ycm = False
    timerid = None
    def handler(self, tp, key):

        if self.timerid:
            pyvim.timerstop(self.timerid)
            self.timerid = None

        if env.syntax in self.wubi_syntax:
            stream.wubi.handler(tp, key)
            return

        self.ycm = False

        getattr(self, tp)(key)

        # ycm 在 .vimrc 中配置了 g:ycm_auto_trigger = 0
        # 所以 ycm 不会自动触发.
        # 并且触发的 key 设置成子  <C-c>

        if self.ycm: # 直接调用 ycm. 比如在 . 或 tab 的后面
            prompt.active()
            #imrc.feedkeys(('\<C-c>', 'm'))

        else: # 延时调用 ycm
            if key.isalpha() or key == '_':
                self.timerid = pyvim.timerstart(750, timer_callback)


class IM_C(IM_Code):
    fts = ['c', 'cpp', 'ch', 'h']
    def cb_dot(self):
        if env.before.endswith('.'):
            feedkeys('\<bs>->')
        else:
            feedkeys('.')

        self.ycm = True
        return True

    def cb_space(self):
        for k in env.before:
            if k == ' ' or k == '\t':
                continue
            feedkeys(' ')
            return True

        feedkeys('\<tab>')
        return True

    def cb_tab( self ):
        if re.search(r'^\s*$', env.before):
            o = '\<tab>'
            feedkeys(o)
        else:
            self.ycm = True
        return True

    def cb_brace(self):#{  }
        if env.after == '' and  env.before.endswith(')'):
            if env.before:
                if env.before[0] in ' \t':
                    feedkeys(' {\<cr>}\<esc>O') # if,for,while
                    return True

            feedkeys('\<cr>{\<cr>}\<up>\<cr>') # function
            return True

        self.double_out('{', '}')
        return True



if __name__ == "__main__":
    pass

