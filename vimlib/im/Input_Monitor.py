#encoding:utf8
import pyvim
import vim
from context import contexts
from imrc import allkeys


class Input_Monitor(object):
    def in_key( self, key ):
        for c in contexts:# 检查所有的context 对象
            if c.in_fsm(key):
                return

    def init_monitor_keys( self ):
        keys=allkeys()
        for map_key, name in keys:
            command='inoremap <expr> %s Input_Monitor( "%s" )' % ( map_key, name)
            vim.command(command)

