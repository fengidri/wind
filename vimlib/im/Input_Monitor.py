#encoding:utf8
import pyvim
import vim
from context import contexts, all_key


class Input_Monitor(object):
    def in_key( self, key ):
        for c in contexts:# 检查所有的context 对象
            if c.in_fsm(key):
                return

#    def all_key( self ):
#        "返回被监控的所有的键的list"
#        return self.context_fsm.all_key( )

    def init_monitor_keys( self ):
        keys=all_key()
        for key in keys:
            if len( key ) > 1 and key.islower():
                map_key = '<%s>' % key
            else:
                map_key = key
            if key == '"':
                key = r'\"'
                map_key = '"'
            command='inoremap <expr> %s input_monitor#Input_Monitor( "%s" )' % ( map_key, key)
            vim.command(command)


        
        




