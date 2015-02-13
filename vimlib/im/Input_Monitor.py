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
        for key in keys:
            if len( key ) > 1 and key.islower():
                map_key = '<%s>' % key
            else:
                map_key = key
            if key == '"':
                key = r'\"'
                map_key = '"'
            command='inoremap <expr> %s Input_Monitor( "%s" )' % ( map_key, key)
            vim.command(command)

