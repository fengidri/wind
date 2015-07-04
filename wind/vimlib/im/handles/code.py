# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:57:20
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from im.handle_base import IM_Base
import pyvim
import re
from im.imrc import feedkeys
import vim
from im.imutils import SelMenu
from pyvim import log as logging

class handle(object):
    def double_out(self, d, b):
        if pyvim.str_after_cursor() == '':
            feedkeys(d + b + '\<left>')
        else:
            feedkeys(d)

    def cb_bracket( self ):#[  ]
        self.double_out('[', ']')

    def cb_parenthess( self ):#(  )
        self.double_out('(', ')')

    def cb_mark( self ):
        self.double_out("'", "'")

    def cb_double_mark( self ):
        self.double_out('"', '"')

    def cb_tab( self ):
        if re.search(r'^\s*$',pyvim.str_before_cursor( )):
            o = '    '
        else:
            o = '\<C-X>\<C-O>\<C-P>'
        feedkeys(o)


    def cb_brace(self):#{  }
        if pyvim.str_after_cursor(  ) == '' and \
            pyvim.str_before_cursor( ).endswith(')'):
                feedkeys('\<cr>{\<cr>}\<up>\<cr>')
                return
        self.double_out('{', '}')

    def cb_dot(self):
        if pyvim.str_before_cursor( ).endswith('.'):
            feedkeys('\<bs>->')
        else:
            feedkeys('.')
        self.complete()

    def cb_underline(self):
        feedkeys('_')
        self.complete()


    def cb_jump(self):
        string=pyvim.str_after_cursor( )
        tag=r'\'"([{}])'

        n_list=[ ]
        for i in tag:
            t=string.find( i )
            if t > -1:
                n_list.append( t )

        if len( n_list ) > 0:
            feedkeys( '\<right>' * ( min( n_list ) +1))



class IM_Code(IM_Base, handle):
    def __init__(self, areas = ['*'] ):
        super(IM_Code, self).__init__()
        self.pmenu = SelMenu()
        #self.AREAS = areas
        self.complete_cmd = 'youcompleteme#OmniComplete'

    def im_upper(self, key):
        IM_Base.im_upper(self, key)
        self.complete()

    def im_lower(self, key):
        IM_Base.im_lower(self, key)
        self.complete()


#    def im(self, key):
#        area = pyvim.syntax_area()
#
#        if not (area in self.AREAS or '*' in self.AREAS):
#            return
#
#        super(IM_Code, self).im(key)
#        self.complete(key)
#        return True




    def is_comp_char(self, key):
        if (key.islower( ) or key.isupper( ) or key in '._'):
            return True
        return False

    def complete(self):
        before = pyvim.str_before_cursor()
        if len(before) < 2:
            return
        if before[-2:] != "->":
            if not self.is_comp_char(before[-1]):
                return
            if not self.is_comp_char(before[-2]):
                return
        if self.complete_cmd:
#            self.pmenu.complete(self.complete_cmd)
            try:
                self.pmenu.complete(self.complete_cmd)
            except:
                logging.error('not found command: %s' , self.complete_cmd)
                self.complete_cmd = ''

if __name__ == "__main__":
    pass

