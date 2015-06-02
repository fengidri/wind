# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 14:57:20
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from inputer_base import IM_Base
import pyvim
import re
import logging
class IM_Code( IM_Base ):
    def __init__(self, areas = ['*'] ):
        super(IM_Code, self).__init__()
        self.pmenu = pyvim.SelMenu()
        self.AREAS = areas
        self.complete_cmd = 'youcompleteme#OmniComplete'

    def im(self, key):
        area = pyvim.syntax_area()

        if not (area in self.AREAS or '*' in self.AREAS):
            return

        super(IM_Code, self).im(key)
        self.complete(key)
        return True

    def double_out(self, d, b):
        if pyvim.str_after_cursor(  ) == '':
            self.output(d + b + '\<left>')
        else:
            self.output(d)


    def cb_bracket( self ):#[  ]
        self.double_out('[', ']')

    def cb_parenthess( self ):#(  )
        self.double_out('(', ')')

    def cb_mark( self ):
        self.double_out("'", "'")

    def cb_double_mark( self ):
        self.double_out('"', '"')

    def cb_tab( self ):
        if pyvim.pumvisible():
            o = '\<C-n>'

        elif re.search(r'^\s*$',pyvim.str_before_cursor( )):
            o = '    '
        else:
            o = '\<C-X>\<C-O>\<C-P>'
        self.output(o)

    def cb_brace( self ):#{  }
        if pyvim.str_after_cursor(  ) == '' and \
            pyvim.str_before_cursor( ).endswith(')'):
                self.output('\<cr>{\<cr>}\<up>\<cr>')
                return
        self.double_out('{', '}')

    def cb_dot(self):
        if pyvim.str_before_cursor( ).endswith('.'):
            pyvim.feedkeys('\<bs>->' ,'n' )
        else:
            pyvim.feedkeys('.' ,'n' )

    def is_comp_char(self, key):
        if len(key) != 1:
            return False
        if (key.islower( ) or key.isupper( ) or key in '._'):
            return True
        return False

    def complete( self, key ):
        if not self.is_comp_char(key):
            return
        before = pyvim.str_before_cursor()
        if len(before) < 2:
            return
        if before[-2:] != "->":
            if not self.is_comp_char(before[-1]):
                return
            if not self.is_comp_char(before[-2]):
                return
        if self.complete_cmd:
            try:
                self.pmenu.complete(self.complete_cmd)
            except:
                self.complete_cmd = ''
                logging.error('not found command: %s' , self.complete_cmd)

if __name__ == "__main__":
    pass

