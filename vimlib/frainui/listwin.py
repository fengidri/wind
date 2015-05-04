# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-04-08 13:51:57
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import node
import vim
import logging
class LISTHOOK(object):
    def OnWinPost(self):
        pass

class LISTOPTIONS(object):
    def open(self):
        l, c = vim.current.window.cursor
        node = self.getnode()
        node._open(l)

    def refresh(self):
        del self.buf[:]
        self.buf[0] = "FrainUI"
        node.LNode.nodes = {}
        self.root = node.Node('root')
        self.addlist()


        self.root.opened = False
        self.root.node_open(1)


    def focus(self, autocreate = True):# 切换到list 窗口,
        # 如果autocreate 为true, 在list窗口已经关闭的情况下, 会自动创建list窗口
        if self.win.valid:
            vim.current.window = self.win
            return True
        else:
            if autocreate:
                self.createwin()
                return True
            return False

    def find(self, names):
        if not self.focus():
            return
        names.insert(0, 'root')
        logging.error('names: %s', names)

        leaf = self.root.find(names)
        if not leaf:
            self.win.cursor = (1, 0)
            return False

        route = leaf.route()
        if not route:
            self.win.cursor = (1, 0)
            return False

        logging.error('route: %s', route)
        for n in route[1:-1]:
            linenu = self.getlinenu(n)
            n.node_open(linenu+1)

        linenu = self.getlinenu(route[-1])
        self.win.cursor = (linenu + 1, 0)
        return True

    def settitle(self, name):#设置vim 窗口的title
        # 如果没有设置name, 则使用第一个root的name
        vim_title = name.replace( ' ', '\\ ')
        vim.command( "set title titlestring=%s" % vim_title )



class LISTWIN(object):
    def createwin(self):
        vim.command( "topleft 25vnew Frain" )
        vim.command( "set ft=frain" )
        w = vim.current.window
        b = vim.current.buffer
        self.OnWinPost()

        return (w, b)

class LISTNODS(object):
    def addlist(self): # 子类实现, 用于增加list窗口的内容
        pass
    def getnode(self, linenu=None): # 从list窗口得到对应的node
        if vim.current.window != self.win:
            logging.error('getnode: current win is not list win')
            return

        if linenu == None: # 没有输入行号, 使用当前行
            line = vim.current.line
        else:
            if linenu >= len(self.buf):
                return
            line = self.buf[linenu]

        line = line.decode('utf8')
        try:
            node_index = int(line.split('<|>')[1])
            return node.LNode.nodes.get(node_index)
        except:
            logging.error('getnode: fail')

    def getlinenu(self, node):
        num = 0
        for linenu, line in enumerate(self.buf):
            try:
                ID = int(line.split('<|>')[1])
                if ID == node.ID:
                    num = linenu
                    break
            except:
                pass
        return num

    def getroots(self):
        return self.root.sub_nodes




class LIST(LISTHOOK, LISTOPTIONS, LISTWIN, LISTNODS):#  list 窗口对象
    def __init__(self):
        node.LNode.ls = self

        self.win, self.buf = self.createwin()
        """
            self.root(Node:root)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
                | ----------------selfNode(rootpath)
        """






    def append(self, node):
        self.root.append(node)

if __name__ == "__main__":
    pass

