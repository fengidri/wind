# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:57:20
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import re
from im.imrc import feedkeys
import vim

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
            env.ycm = True
        return True


    def cb_brace(self):#{  }
        if env.after == '' and  env.before.endswith(')'):
            feedkeys('\<cr>{\<cr>}\<up>\<cr>')
            return True
        self.double_out('{', '}')
        return True

    def cb_dot(self):
        if env.before.endswith('.'):
            feedkeys('\<bs>->')
        else:
            feedkeys('.')

        env.ycm = True
        return True

    def cb_underline(self):
        feedkeys('_')
        return True


    def cb_jump(self):
        string = env.after
        tag=r'\'"([{}])'

        n_list=[ ]
        for i in tag:
            t=string.find( i )
            if t > -1:
                n_list.append( t )

        if len( n_list ) > 0:
            feedkeys( '\<right>' * ( min( n_list ) +1))
        return True

    def cb_backspace(self):
        #for c in env.before:
        #    if c != ' ':
        #        break
        #else: #
        #    l = len(env.before)
        #    if l != 0:
        #        left = l % 4
        #        if left == 0:
        #            left = 4
        #        feedkeys('\<bs>' * left)
        #        return True

        feedkeys('\<bs>')
        return True

import im.handler as handler
import im.imrc as imrc

class IM_Code(im.keybase.BaseEnd, handle):
    wubi_syntax = ['Constant', 'CCommentDesc', 'CCommentArg', 'Comment', 'String']
    fts = ['c', 'cpp', 'python', 'javascript', 'ch', 'vim', 'html', 'sh']

    def handler(self, tp, key):
        if pyvim.pumvisible():
            getattr(handler.HD_Prompt, tp)(key)
            return

        imrc.complete_timer.stop()

        if env.syntax in self.wubi_syntax:
            handler.HD_WubiStream.handler(tp, key)
            return

        getattr(self, tp)(key)

        if env.ycm:
            imrc.feedkeys(('\<C-c>', 'm'))
        else:
            if (key.isalpha() or key == '_'):
                imrc.complete_timer.start()

class IM_Lua(IM_Code):
    def cb_dot(self):
        feedkeys('.')
        return True


if __name__ == "__main__":
    pass

