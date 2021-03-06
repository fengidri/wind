# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-01-21 12:27:00
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import sqlite3
wbtxt = os.path.join(os.path.dirname(__file__), 'wubi.txt').replace('\\','/')
wbdb = os.path.join(os.path.dirname(__file__), 'wubi.db').replace('\\','/')


class StopFind(Exception):
    pass
class NotFound(Exception):
    pass

class node(dict):
    def __init__(self, ctx = None, count = 0):
        dict.__init__(self)
        self.ctx = {} # 还要记录每一个词的使用次数
        if ctx:
            self.append(ctx, count)

    def append(self, ctx, count):
        "增加节点的私用数据"
        self.ctx[ctx] = count

    def wb_find(self, patten):
        k = patten[0]
        nt = self.get(k)
        if nt == None:
            raise NotFound
        if len(patten) == 1:
            return nt  # 根据patten 找到当前node
        else:
            return nt.wb_find(patten[1:])

    def wb_words(self):# 返回按使用次数排序的list
        keys = self.ctx.keys()
        return sorted(keys, key=lambda x: self.ctx.get(x), reverse=True)

    def wb_wordsc(self): # 返回值带有使用次数构成dict
        return self.ctx

    def wb_associate(self):#返回值复杂, 包含有联想的key, 还有带有次数的dict
        ass = []
        for k, c  in self.items():
            for w, c in c.wb_wordsc().items():
                ass.append((w, k, c))

        return sorted(ass, key = lambda x:x[2], reverse=True)

    def addcount(self, key, w):
        "为指定的patten 下对应的多词的使用次数朝廷统计"
        if w not in self.ctx:
            return

        self.ctx[w] += 1
        sql_count = "update wbdb set count=%s  where key='%s' and word='%s'"
        s = sql_count % (self.ctx[w], key, w)
        print(sql_count)

        cx = sqlite3.connect(wbdb)
        cu = cx.cursor()
        cu.execute(s)
        cx.commit()
        cx.close()


def tree_add(patten, words, count):
    fa = ROOT
    le = len(patten)
    index = 0
    for p in patten:
        index += 1
        n = fa.get(p)
        if n == None:
            if index == le:
                n = node(words, count)
            else:
                n = node()
            fa[p] = n
        else:
            if index == le:
                n.append(words, count)
        fa = n


def create_table():
    "根据txt 格式的码表文件生成sqlite 数据库格式的数据文件"
    cx = sqlite3.connect(wbdb)
    cu = cx.cursor()

    sql_create_table = """create table wbdb(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   key varchar(4),
   word text,
   count INTEGER default 0
   );"""

    sql_insert_table = "insert into  wbdb(key, word) values('%s', '%s')";

    cu.execute(sql_create_table)
    cx.commit()

    for line in open(wbtxt).readlines():
        line = line.decode('utf8')
        word = line.split()
        key = word[0]
        del word[0]
        for w in word:
            ss = sql_insert_table % (key, w)
            cu.execute(ss)
    cx.commit()#这里统一执行可以大大提高效率
    cx.close()




if __name__ != "__main__":
    # 做为模块时自动加载数据结构
    ROOT = node([])
    cx = sqlite3.connect(wbdb)
    cu = cx.cursor()

    sql_search = "select key, word, count from wbdb"
    cu.execute(sql_search)
    for line in cu.fetchall():
        key = line[0]
        word = line[1]
        count = line[2]
        tree_add(key, word, count)
    cx.close()

else:
    # 创建需要的表格式
    create_table()
