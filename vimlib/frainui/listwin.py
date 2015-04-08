# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import node
import vim
import logging

class LISTOPTIONS(object):
    def open(self):
        l, c = vim.current.window.cursor
        node = self.getnode()
        node._open(l)

    def refresh(self):
        del self.buf[:]
        vim.current.buffer[0] = "FrainUI"
        self.root._open(1)

    def focus(self, autocreate = True):
        if self.win.valid():
            vim.current.window = data.LISTWIN.win
            return True
        else:
            if autocreate:
                self.createwin()
                return True
            return False

class LISTWIN(object):
    def createwin(self):
        vim.command( "topleft 25vnew frain" )
        vim.command( "set ft=paths_exp" )
        w = vim.current.window
        b = vim.current.buffer
        return (w, b)

class LISTNODS(object):
    def getnode(self, linenu=None): # 从list窗口得到对应的node
        if vim.current.window != self.win:
            logging.error('getnode: current win is not list win')
            return

        if linenu == None: # 没有输入行号, 使用当前行
            line = vim.current.line
        else:
            line = self.buf[linenu]

        line = line.decode('utf8')
        try:
            node_index = int(line.split('<|>')[1])
            return node.LNode.nodes.get(node_index)
        except:
            logging.error('getnode: fail')



class LIST(LISTOPTIONS, LISTWIN, LISTNODS):#  list 窗口对象
    def __init__(self):
        self.win, self.buf = self.createwin()
        self.root = node.Node('root')
        node.LNode.ls = self


    def append(self, node):
        self.root.append(node)

if __name__ == "__main__":
    pass

