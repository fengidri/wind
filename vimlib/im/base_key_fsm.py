#encoding:utf8
import pyvim
import vim
import re
import imrc
import string
#import wbtree
import urllib2
import json
class Base_Fsm( object ):
    def __init__(self):
        self.key_map={}
        for c in string.digits:
            self.key_map[c] = self.digit
        for c in string.ascii_lowercase:
            self.key_map[c] = self.lower_letter
        for c in string.ascii_uppercase:
            self.key_map[c] = self.upper_letter

        self.punc_map={
            "(" : self.parenthess,
            "[" : self.bracket,
            "{" : self.brace,
            "'" : self.mark,
            "," : self.comma,
            ";" : self.semicolon,
            "-" : self.minus,
            "_" : self.underline,
            "+" : self.add,
            "%" : self.precent,
            "&" : self.and_,
            "<" : self.lt,
            ">" : self.gt,
            "^" : self.cat,
            "!" : self.not_,
            "." : self.dot,
            "/" : self.slash,
            "=" : self.eq,
            '"' : self.double_mark,
            'tab' : self.tab,
            'c-j' : self.c_j,
            'bs' : self.backspace,
            'cr' : self.enter,
            'space': self.space,
            'esc': self.esc
            }
            #}}}
    def Leave(self):
        pass
    def Enter(self):
        pass
    def in_fsm( self, key):
        self.key= key
        callback=self.key_map.get(key, self.punc)
        callback()
    def all_key( self ):
        keys=self.key_map.keys( )
        keys.extend( self.punc_map.keys())
        return keys

 
    def digit( self ):
        pyvim.feedkeys( self.key ,'n' )

    def upper_letter( self ):
        pyvim.feedkeys( self.key  ,'n' )

    def lower_letter( self ):
        pyvim.feedkeys( self.key ,'n'  )

    def punc(self):
        callback=self.punc_map.get( self.key, None)

        if callback:
            callback()

    def parenthess(self):
        pyvim.feedkeys("(" ,'n' )
    def bracket(self):
        pyvim.feedkeys('[' ,'n' )
    def brace(self):
        pyvim.feedkeys('{' ,'n' )
    def mark(self):
        pyvim.feedkeys("'" ,'n' )
    def comma(self):
        pyvim.feedkeys(',' ,'n' )
    def semicolon(self):
        pyvim.feedkeys(';' ,'n' )
    def minus(self):
        pyvim.feedkeys('-' ,'n' )
    def add(self):
        pyvim.feedkeys('+' ,'n' )
    def precent(self):
        pyvim.feedkeys('%' ,'n' )
    def and_(self):
        pyvim.feedkeys('&' ,'n' )
    def lt(self):
        pyvim.feedkeys('<' ,'n' )
    def gt(self):
        pyvim.feedkeys('>' ,'n' )
    def cat(self):
        pyvim.feedkeys('^' ,'n' )
    def not_(self):
        pyvim.feedkeys('!' ,'n' )
    def dot(self):
        pyvim.feedkeys('.' ,'n' )
    def underline( self ):
        pyvim.feedkeys('_' ,'n' )

    def slash(self):
        pyvim.feedkeys('/' ,'n' )
    def eq(self):
        pyvim.feedkeys('=' ,'n' )
    def double_mark(self):
        pyvim.feedkeys('"' ,'n' )
    def tab(self):
        pyvim.feedkeys('    ' ,'n' )

        
    def c_j(self):
        string=pyvim.str_after_cursor( )
        tag=r'\'"([{}])'

        n_list=[ ]
        for i in tag:
            t=string.find( i )
            if t > -1:
                n_list.append( t )

        if len( n_list ) > 0:
            pyvim.feedkeys( '\<right>' * ( min( n_list ) +1))

    def backspace(self):
        pyvim.feedkeys(r'\<BS>','n')
    def enter(self):
        pyvim.feedkeys(r'\<CR>' ,'n')
    def space(self):
        pyvim.feedkeys(r'\<space>', 'n')
    def esc( self ):
        pyvim.feedkeys('\<esc>' ,'n' )

    def fsm_name(self):
        return "base"
        
class Base_Key_Fsm( Base_Fsm ):
    def fsm_name(self):
        return "base"
    def tab(self):
        if pyvim.pumvisible():
            pyvim.feedkeys('\<C-n>' ,'n' )
        else:
            pyvim.feedkeys('    ' ,'n' )

class Html_Key_Fsm( Base_Fsm ):
    def fsm_name(self):
        return "html"
    def gt(self):
        regex = "<(\w+)[^>]+$"
        match = re.search(regex, pyvim.str_before_cursor())

        if match:
            flag = match.group(1)
            s = '></%s>%s' % ( flag,  "\<left>" * (len(flag) + 3))
            pyvim.feedkeys( s,'n' )
        else:
            Base_Fsm.gt(self)
class Base_Code_Fsm( Base_Fsm ):
    def fsm_name(self):
        return "code"

    def tab( self ):
        if pyvim.pumvisible():
            pyvim.feedkeys('\<C-n>' ,'n' )
            return 0

        if re.search(r'^\s*$',pyvim.str_before_cursor( )):
            pyvim.feedkeys( '    ')
        else:
            pyvim.feedkeys('\<C-X>\<C-O>\<C-P>' )

    def bracket( self ):#[  ]
        if pyvim.str_after_cursor(  ) == '':
            pyvim.feedkeys( '[]', 'n')
            pyvim.feedkeys('\<left>')
        else:
            pyvim.feedkeys( '[', 'n')

    def parenthess( self ):#(  )
        if pyvim.str_after_cursor(  ) == '':
            pyvim.feedkeys('()', 'n')
            pyvim.feedkeys('\<left>')
        else:
            pyvim.feedkeys('(', 'n')
    
    def brace( self ):#{  }
        if pyvim.str_after_cursor(  ) == '':
            if pyvim.str_before_cursor( ).endswith( ')'):
                pyvim.feedkeys( '\<cr>{\<cr>}\<up>\<cr>','n')
            else:
                pyvim.feedkeys( '{}\<left>', 'n')
        else:
            pyvim.feedkeys('{', 'n')
    
    def mark( self ):
        if pyvim.str_after_cursor(  ) == '':
            pyvim.feedkeys("\<c-v>'\<c-v>'\<left>")
        else:
            pyvim.feedkeys("\<c-v>'")
    
    def double_mark( self ):
        str_after=pyvim.str_after_cursor(  )
        if  str_after == '':
            pyvim.feedkeys( r'""\<left>','n')
            return 0

        if str_after[0] == '"':
            pyvim.feedkeys( r'""\<left>','n')
            return 0

        pyvim.feedkeys( '"','n')
    def dot(self):
        if pyvim.str_before_cursor( ).endswith('.'):
            pyvim.feedkeys('\<bs>->' ,'n' )
        else:
            pyvim.feedkeys('.' ,'n' )

class _wubi_seach( object ):
    def __init__(self):
        self.cache={  }

    def search_from_db(self, patten):
        try:
            r = urllib2.urlopen("http://localhost/wubi/search?patten=%s" %
                patten)
            return json.loads(r.read())
        except Exception, e:
            pyvim.echoline(str(e))
            return ([], [])


    def search( self , buf):
        '得到备选的字词'

        patten = ''.join( buf )

        words= self.cache.get( patten )
    
        if  words:
            return words

        w = self.search_from_db(patten)
        self.cache[ patten ] = w

        return w
    def setcount(self, patten, num):
            w, ass = self.cache.pop(patten)
            ww = w[num]
            url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
                    ww.encode('utf8'))
            try:
                urllib2.urlopen(url)
            except Exception, e:
                pyvim.echoline(str(e))
        



class Wubi( Base_Key_Fsm):
    def fsm_name(self):
        return "wubi"
    def Enter(self):
        del self.buffer[:]
        pyvim.pmenu.check_omnifunc( 'input_monitor#OmniComplete' )

    def Leave(self):
        pass

    def __init__(self):
        super(Wubi, self).__init__()
        self.buffer=[]
        self.search=  _wubi_seach( )

    def in_fsm( self, key):
        self.key= key

        callback=self.key_map.get(key, self.punc)
        callback()

    def wubi(self):
        self.match_words  = self.result( *self.search.search(self.buffer) ) 

        vim.vars["omniresult"] = self.match_words
        #imrc.wubi_match_words= self.match_words



    def result(self, words, associate):
        '组成vim 智能补全要求的形式，这一步只是py形式的数据，vim要求是vim的形式'
        patten = ''.join(self.buffer)

        items=[{"word": " " ,"abbr":"%s                  " %  patten }]

        if len( self.buffer ) > 4:
            return items

        i = 0
        for w in words:
            i += 1
            items.append({"word":w, "abbr":"%s.%s"%(i, w)})

        for w, k, c  in associate:
            i += 1
            items.append(
                    {"word":w, 
                        "abbr":"%s.%s %s"%(i, w, k)}
                    )

        return items



    def backspace(self):
        if not pyvim.pumvisible():
            pyvim.feedkeys('\<bs>', 'n')
            return 0

        if len( self.buffer ) > 1:
            self.buffer.pop()
            self.wubi()
            pyvim.pmenu.show( 'input_monitor#OmniComplete')
        else:
            del self.buffer[:]
            pyvim.pmenu.cencel( )

   
    def enter(self):
        if pyvim.pumvisible():
            pyvim.feedkeys(r'%s\<C-e>' % ''.join(self.buffer),'n')
            del self.buffer[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def digit( self ):
        if pyvim.pumvisible():

            self.search.setcount(''.join(self.buffer), int(self.key) -1)
            pyvim.pmenu.select( int(self.key) )
            del self.buffer[:]
            return 0
        pyvim.feedkeys( self.key ,'n')


    def upper_letter( self ):
        del self.buffer[:]
        pyvim.feedkeys( self.key  ,'n' )


    def punc(self):
        callback=self.punc_map.get(self.key, None)

        if callback:
            callback()

    def lower_letter( self ):
        self.buffer.append( self.key )

        self.wubi()
        pyvim.pmenu.show( 'input_monitor#OmniComplete')

    def space(self):
        del self.buffer[:]
        if pyvim.pumvisible():
            pyvim.pmenu.select( 1 )
            return 0
        pyvim.feedkeys('\<space>', 'n')

    def esc( self ):
        del self.buffer[:]
        pyvim.feedkeys( '\<esc>','n')

        








if not __name__=="__main__":
    key_fsm=[Base_Key_Fsm( ), Base_Code_Fsm(), Wubi(), Html_Key_Fsm()]
