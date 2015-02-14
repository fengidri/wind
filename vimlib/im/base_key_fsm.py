#encoding:utf8
import pyvim
import vim
import re
import string
import imrc

import urllib2
import json

class Base_Fsm( object ):
    def __init__(self):
        #处理重载的key
        self.cbs = {}
        self.simple_key = imrc.digits + imrc.lowerletter + imrc.upperletter
        for attr in dir(self):
            if not attr.startswith('cb_'):
                continue
            vname = attr[3:]

            self.cbs[vname] = getattr(self, attr)


    def Enter(self):
        pass

    def Leave(self):
        pass

    def fsm_name(self):
        return "base"

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

class Base_Key_Fsm(Base_Fsm):
    pass

class Html_Key_Fsm( Base_Fsm ):
    def fsm_name(self):
        return "html"
    def cb_gt(self):
        regex = "<(\w+)[^>]+$"
        match = re.search(regex, pyvim.str_before_cursor())

        if match:
            flag = match.group(1)
            s = '></%s>%s' % ( flag,  "\<left>" * (len(flag) + 3))
            pyvim.feedkeys( s,'n' )
        else:
            Base_Fsm.gt(self)

class Base_Code_Fsm( Base_Fsm ):
    def __init__(self):
        super(Base_Code_Fsm, self).__init__()
        self.pmenu = pyvim.SelMenu()

    def fsm_name(self):
        return "code"

    def in_fsm(self, key):
        super(Base_Code_Fsm, self).in_fsm(key)
        self.complete(key)

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
        self.pmenu.complete('youcompleteme#OmniComplete')

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


    def search( self , patten):
        '得到备选的字词'
        words= self.cache.get( patten )
    
        if  words:
            return words

        w = self.search_from_db(patten)
        self.cache[ patten ] = w

        return w
    def setcount(self, patten, num):
        w, ass = self.cache.pop(patten)
        if len(w) -1 < num:
            return
        ww = w[num]
        url = "http://localhost/wubi/setcount?patten=%s&word=%s" % (patten,
                ww.encode('utf8'))
        try:
            urllib2.urlopen(url)
        except Exception, e:
            pyvim.echoline(str(e))

    def wubi(self, patten):
        return self.result(patten, *self.search(patten)) 

    def result(self, patten, words, associate):
        '组成vim 智能补全要求的形式，这一步只是py形式的数据，vim要求是vim的形式'

        items=[{"word": " " ,"abbr":"%s                  " %  patten }]

        if len( patten ) > 4:
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

class Wubi( Base_Key_Fsm, _wubi_seach):
    def fsm_name(self):
        return "wubi"

    def Enter(self):
        del self.buffer[:]

    def Leave(self):
        pass

    def __init__(self):
        Base_Key_Fsm.__init__(self)
        _wubi_seach.__init__(self)
        self.buffer=[]
        self.pmenu = pyvim.SelMenu()

    def cb_backspace(self):
        if not pyvim.pumvisible():
            pyvim.feedkeys('\<bs>', 'n')
            return 0

        if len( self.buffer ) > 1:
            self.buffer.pop()
            self.patten = ''.join(self.buffer)
            self.pmenu.show(self.wubi(self.patten), 0)
        else:
            del self.buffer[:]
            self.pmenu.cencel( )

   
    def cb_enter(self):
        if pyvim.pumvisible():
            pyvim.feedkeys(r'%s\<C-e>' % self.patten,'n')
            del self.buffer[ : ]
            return 0
        pyvim.feedkeys(r'\<cr>' ,'n')

    def cb_space(self): 
        del self.buffer[:]
        if pyvim.pumvisible():
            self.pmenu.select( 1 )
            return 0
        pyvim.feedkeys('\<space>', 'n')

    def cb_esc( self ):
        del self.buffer[:]
        pyvim.feedkeys( '\<esc>','n')

    def in_fsm(self, key):
        self.key = key
        if key in self.cbs: #如果有对应的重载方法
            self.cbs.get(key)()

        elif key in imrc.digits:
            self.digit()

        elif key in imrc.lowerletter:
            self.lower_letter()

        elif key in imrc.upperletter:
            self.upper_letter()

        elif key in imrc.puncs: # 符号key
            self.output(imrc.puncs[key][0])

    def digit( self ):
        if pyvim.pumvisible():

            self.setcount(self.patten, int(self.key) -1)
            self.pmenu.select( int(self.key) )
            del self.buffer[:]
            return 0
        pyvim.feedkeys( self.key ,'n')

    def upper_letter( self ):
        del self.buffer[:]
        pyvim.feedkeys( self.key  ,'n' )

    def lower_letter( self ):
        self.buffer.append( self.key )
        self.patten = ''.join(self.buffer)
        self.pmenu.show(self.wubi(self.patten), 0)


if not __name__=="__main__":
    key_fsm=[Base_Key_Fsm( ), Base_Code_Fsm(), Wubi(), Html_Key_Fsm()]




