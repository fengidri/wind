#encoding:utf8
"""
  高亮当前word
"""
import pyvim
import vim
class _input_post( ):
    def __init__( self ):
        self.lastword = ''
        self.match_id = ''
        self.ids = {}

        vim.command("hi CurrentWord guibg=#3f3853 gui=None")
        vim.command("syn keyword CurrentWord CurrentWord")

    def input_post( self ):
        self.hi_current_word( )

    def hi_current_word( self ):
        current = pyvim.current_word(from_vim=False)

        if current.isspace() or current == '':
            return -2

        if len(current) < 4:
            return

        if self.lastword == current:
            return -1
        self.lastword = current

        mid = self.ids.get(vim.current.buffer)
        if mid:
            fu = vim.Function("matchdelete")(mid)

        fu = vim.Function("matchadd")
        self.ids[vim.current.buffer] = fu("CurrentWord", "\<%s\>" % current, 11)

input_post = _input_post( )

@pyvim.event("CursorMovedI")
def run():
    input_post.input_post(  )

#@pyvim.event("CursorMoved")
#def run():
#    input_post.input_post(  )

