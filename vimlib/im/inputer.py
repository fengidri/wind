# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 15:14:23
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import imrc

class Base_Key_Fsm( object ):
    def __init__(self):
        #处理重载的key
        self.cbs = {}
        self.simple_key = imrc.digits + imrc.lowerletter + imrc.upperletter
        for attr in dir(self):
            if not attr.startswith('cb_'):
                continue
            vname = attr[3:]

            self.cbs[vname] = getattr(self, attr)


    def output(self, out):
        pyvim.feedkeys( out ,'n' )

    def in_fsm( self, key):
        if key in self.cbs: #如果有对应的重载方法
            self.cbs.get(key)()

        elif key in self.simple_key: # 简单的key
            self.output(key)

        elif key in imrc.puncs: # 符号key
            self.output(imrc.puncs.get(key)[1])

    def cb_tab(self):
        if pyvim.pumvisible():
            o = '\<C-n>'
        else:
            o = '    '
        self.output(o)

    def cb_jump(self):
        string=pyvim.str_after_cursor( )
        tag=r'\'"([{}])'

        n_list=[ ]
        for i in tag:
            t=string.find( i )
            if t > -1:
                n_list.append( t )

        if len( n_list ) > 0:
            pyvim.feedkeys( '\<right>' * ( min( n_list ) +1), 'n')

if __name__ == "__main__":
    pass

