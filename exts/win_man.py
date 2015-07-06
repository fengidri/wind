import pyvim
import vim
class ClearAllWin( pyvim.command ):
    def run( self ):
        locale_w = vim.current.window
        for w in vim.windows:
            if w == locale_w:
                continue
            if vim.current.buffer.options['buftype'] != "":
                continue
            if w.buffer.name.find( '__Tag_List__' ) > 0:
                continue
            if w.buffer.name.find( 'NERD_tree_' ) > 0:
                continue
            vim.current.window = w
            vim.command( "close" )
        vim.current.window = locale_w
    
