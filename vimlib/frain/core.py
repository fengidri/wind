# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-31 11:28:09
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

class LIST(object):

    def __init__(self):
        self.win = vim.current.window
        self.buf = vim.current.buffer

    def getnode(self, linenu=None):
        if linenu == None: # 没有输入行号, 使用当前行
            line = vim.current.line
        else:
            line = self.buf[linenu]
        line = line.decode('utf8')
        try:
            node_index = int(line.split('<|>')[1])
            return LNode.nodes.get(node_index)
        except:
            pass




class LNode(object):# Node与Leaf 的父类
    ls = None
    level = 0
    father = None

    nodes = {}  # 所有的节点, 除了可以保存在树形的结构中外, 全部在这里有索引
    ID = 0
    def __init__(self):
        # 新的实例, 要生成ID, 并加入到nodes中去
        self.ID = LNode.ID
        LNode.ID += 1
        LNode.nodes[self.ID] = self

    def show(self):
        return "%s +%s/" % ("  " * (self.level  -1), self.name)

    def find(self, names):# 查找一个节点, 目标如['etc', 'nginx', 'conf.d']
        # 好喜欢这个函数啊!! 哈哈, good
        if self.level >= len(names):#超出层级了
            return

        if self.name != names[self.level]:# 当前不节点是节查找中的一个节点
            return

        if self.level = len(names) -1 : # 当前节点是是节查找的最后一个
            return self

        if not hasattr(self, 'sub_nodes'): # 如果是leaf 直接返回
            return

        # 这个处理是针对于node 节点的
        for n in self.sub_nodes: # node 在子节点中找
            m = n.find(names)
            if m:
                return m
        else:
            return #子节点中没有找到

    def route(self): # 返回从最高层, 到本节点的路径中的所有的节点
        # 又是一个好函数
        rt = [self]
        fa = self.father
        while fa:
            rt.insert(0, fa)
            fa = fa.father
        return rt




    


class Node(LNode):
    def __init__(self, name):
        LNode.__init__(self)
        self.sub_nodes = []
        self.name = ''
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
        return "%s %s%s/" % ("  " * (self.level  -1), flag, self.name)

    def _open(self, linenu): # 回车 TODO
        if self.opened: return
        self.opened = True

        for n in self.sub_nodes:
            self.listbuffer.append(n.show(), linenu)
            linenu += 1

    def _close(self): # 
        if not self.opened: return
        self.opened = False

        for n in self.sub_nodes:
            listbuffer.append(n.show(), linenu)
            linenu += 1

class Leaf(LNode):
    def __init__(self, name):
        LNode.__init__(self)
        self.name  = name

    def show(self):
        return "%s  %s/" % ("  " * (self.level  -1), self.name)

    def _open(self):#TODO
        vim.command( "noautocmd wincmd p" )
        if self.listwin = vim.current.window:
            return

        self.open()

    def open(self):# upstream完成叶节点在编辑区的处理方式
        pass




if __name__ == "__main__":
    pass

