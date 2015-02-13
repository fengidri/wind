# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-13 18:22:39
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


from im.base_key_fsm import key_fsm
from im.imrc import fa_rule
import pyvim
import logging
import vim
logging.basicConfig(filename="/tmp/vimlog", level=logging.DEBUG)


class Rule(object):
    def __init__(self, lines):
        self.default_fsm = None
        self.fm = {}
        lines = [line.split() for line in lines]
        try:
            for syn, fn in lines:
                if syn == "*":
                    self.default_fsm = fn
                    continue
                self.fm[syn] = fn
        except:
            pass
    def get(self, syn):
        return self.fm.get(syn, self.default_fsm)

class Rules(object):
    def __init__(self, fa_rule):
        self.rules = {}
        self.default_fsm = None
        rules = fa_rule.split("\n>")
        for rule in rules:
            lines = rule.split('\n')
            tmp = Rule(lines[1:])
            for f in lines[0].split(','):
                if f == "*":
                    self.default_fsm = tmp
                    continue
                self.rules[f] = tmp
    def get(self, f, syn):
        r = self.rules.get(f, self.default_fsm)
        if not r:
            return 'base'
        m =  r.get(syn)
        if not m:
            return 'base'
        return m


        




class Base_Context_Fsm( object ):
    def __init__(self):
        self.pmenu = pyvim.SelMenu()
        self.rules = Rules(fa_rule)

        self.all_fsm = {}
        for fsm in key_fsm:
            self.all_fsm[fsm.fsm_name()] = fsm

        self.current = (None, None) #当前的(文件类型, 语法区)

        self.fsm_name = "base"
        self.fsm = self.all_fsm.get(self.fsm_name)
    
    def in_fsm( self,  key):
        ft = vim.eval('&ft')
        area = pyvim.syntax_area()

        '当在多个key fsm之间进行切换时，在切入与切出时，可能要执行一些动作'
        '在基础状态机中有Enter Leave函数分应这两种情况'
        if self.current  != (ft, area):
            self.current = (ft, area)

            self.fsm.Leave()
            fs_name = self.rules.get(ft, area)
            self.fsm_name = fs_name
            self.fsm = self.all_fsm.get(fs_name)
            self.fsm.Enter()
            logging.info("Switch fsm ft:%s, area:%s, fsname:%s.", ft, area, fs_name)

        self.fsm.in_fsm(key)
        self.complete(key)
        return True

    def is_comp_char(self, key):
        if (key.islower( ) or key.isupper( ) or key in '._'):
            return True
        return False

    def complete( self, key ):


        if self.fsm_name != "code":
            return

        if len(key) != 1:
            return
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


    def all_key( self ):
        return self.fsm.all_key( )
        


if __name__ == "__main__":
    pass

