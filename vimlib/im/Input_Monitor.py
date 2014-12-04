#encoding:utf8
import pyvim
import vim
from im.base_context_fsm import Base_Context_Fsm


class Input_Monitor(object):
    def __init__( self ):
        self.context_fsm=Base_Context_Fsm( )
        self.ft = ""


    def filetype( self ):
        filetype= vim.eval( '&ft' )
        self.ft = filetype


    def in_key( self, key ):
        self.context_fsm.in_fsm(self.ft, pyvim.syntax_area(), key)



    def all_key( self ):
        "返回被监控的所有的键的list"
        return self.context_fsm.all_key( )

    def init_monitor_keys( self ):
        keys=self.all_key()
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


        
        




