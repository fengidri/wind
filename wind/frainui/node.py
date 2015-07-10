# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:28:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from pyvim import log as logging
import vim
class Item(object):# Node与Leaf 的父类
    lswin      = None # 指向list.win对象.
    level   = 0
    father  = None  # 指向father 对象

    nodes   = {}  # 所有的节点, 除了可以保存在树形的结构中外, 全部在这里有索引
    ID      = 0
    def __init__(self):
        # 新的实例, 要生成ID, 并加入到nodes中去
        self.ID = Item.ID
        Item.nodes[self.ID] = self
        Item.ID += 1

    @classmethod
    def getnode(cls, linenu = None):
        if not cls.lswin:
            return
        if not cls.lswin.is_focus():
            return

        if linenu == None: # 没有输入行号, 使用当前行
            line = vim.current.line
        else:
            if linenu >= cls.lswin.linenu():
                return
            line = cls.lswin.getline(linenu)

        line = line.decode('utf8')
        try:
            node_index = int(line.split('<|>')[1])
            return cls.nodes.get(node_index)
        except:
            logging.error('getnode: fail')



    def find(self, names):
        " 查找一个节点, 目标如['etc', 'nginx', 'conf.d']"

        # 好喜欢这个函数啊!! 哈哈, good
        if self.level >= len(names):#超出层级了
            return

        if self.name != names[self.level]:# 当前不节点是节查找中的一个节点
            return

        if self.level == len(names) -1 : # 当前节点是是节查找的最后一个
            return self

        if not hasattr(self, 'sub_nodes'): # 如果是leaf 直接返回
            return

        # 这个处理是针对于node 节点的
        self.LS_Node_Init()
        for n in self.sub_nodes: # node 在子节点中找
            m = n.find(names)
            if m:
                return m
        else:
            return #子节点中没有找到

    def route(self):
        # 返回从最高层, 到本节点的路径中的所有的节点(包括自身)
        # 又是一个好函数
        rt = [self]
        fa = self.father
        while fa:
            rt.insert(0, fa)
            fa = fa.father
        return rt

    def OpenPre(self):
        return True

    def OpenPost(self):
        return True

    def ClosePre(self):
        return True

    def ClosePost(self):
        return True






class Node(Item):
    def LS_Node_Init(self):# 初始sub_nodes数据, 不是事件
        pass


    def OpenPre(self):
        self.LS_Node_Init()
        return True

    def __init__(self, name):
        Item.__init__(self)
        self.sub_nodes = []
        self.name = name
        self.opened = False

    def append(self, node):
        node.level = self.level + 1 # 用于方便得到层级关系
        node.father = self # 子node 要记录自己的father

        self.sub_nodes.append(node)

    def show(self):
        if self.opened:
            flag = '-'
        else:
            flag = '+'
        return "%s%s%s/<|>%s" % ("  " * (self.level  -1), flag, self.name,
                self.ID)

    def _open(self, linenu): # 回车 TODO
        if self.opened:
            self.node_close(linenu)
        else:
            self.node_open(linenu)

    def node_open(self, linenu):
        if self.opened: return
        self.opened = True


        if not self.OpenPre(): return


        buf = self.lswin.b
        buf[linenu - 1] = buf[linenu - 1].replace('+', '-', 1)

        for n in self.sub_nodes:
            if hasattr(n, 'opened'):
                n.opened = False
            self.lswin.b.append(n.show(), linenu)
            linenu += 1


        self.OpenPost()

    def node_close(self, linenu): #
        if not self.opened: return
        logging.error('close')
        self.opened = False

        if not self.ClosePre(): return

        buf = self.lswin.b
        buf[linenu - 1] = buf[linenu - 1].replace('-', '+', 1)

        start = linenu
        while True:
            node = Item.getnode(linenu)
            if not node:
                break
            if node.level <= self.level:
                break
            linenu += 1
        end  = linenu

        if end > start:
            del self.lswin.b[start: end]

        self.ClosePost()

class Leaf(Item):
    def __init__(self, name):
        Item.__init__(self)
        self.name  = name

    def show(self):
        return "%s %s<|>%s" % ("  " * (self.level  -1), self.name, self.ID)

    def _open(self, linenu):#TODO
        vim.command( "noautocmd wincmd p" )
        if self.lswin.is_focus():
            return

        if not self.OpenPre(): return

        self.LS_Leaf_Edit()

        self.OpenPost()

    def LS_Leaf_Edit(self):# upstream完成叶节点在编辑区的处理方式
        pass




if __name__ == "__main__":
    pass

