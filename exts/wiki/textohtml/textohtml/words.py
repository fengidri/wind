# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import logging
class Word( object ):
    "词法对象"
    TEX_CHAR = ['%','#','$','&','{','}', '^', '_', '~', '[', ']', ' ', '\n']
    TEX_CONTROL_CHAR = ['#', '$', '%', '^', '&', '_', '{', '}', '~', '\\']
    TEX_CONTROL_PUNC = [' ']


    TYPE_CONTROL = 1  # 控制序列
    TYPE_PUNC    = 2  # 特殊符号
    TYPE_TEXT    = 3  # 文字
    TYPE_CPUNC   = 4  # 形如\# \$ \% \^ \& \_ \{ \} \~ \\
    TYPE_COMMENT = 5
    TYPE_TYPING  = 6

    def __init__(self, t, l, name, pos):
        self.pos = pos

        self.len = l   # 长度
        self.type = t   # 对应类型
        self.nm = name


    def name(self):
        return self.nm

    def showname(self):#
        nm = self.nm
        if nm == '\n': nm= '\\n'
        if nm == ' ': nm = '\\space'
        return nm
    def show(self):
        return "name:%s, line:%s column:%s"% (self.showname(),
                self.pos[0], self.pos[1])



class Source(object): # 对于souce 进行包装
    def __init__(self, source):
        self.pos = 0
        self.source = source
        self.length = len(source)

    def getchar(self): # 得到当前的char
        if self.pos >= self.length:
            return None
        return self.source[self.pos]

    def update(self): # 记数器+1
        self.pos += 1



class PostionCounter(object): # 计算当前的位置
    def __init__(self, source, words):
        self.line = 1
        self.col = 0
        self.source = source
        self.col_start = 0
        self.words = words

    def update(self, char):
        if char == '\n':
            self.line += 1
            self.col_start = self.source.pos

    def get_pos(self):
        col = self.source.pos - self.col_start
        return (self.line, col, self.source.pos, self.words.end)


def get_control(source, pos):
    length = 1

    name = []
    name.append(source.getchar())

    source.update()
    tp = Word.TYPE_CONTROL

    while source.getchar():
        char = source.getchar()
        if length == 1:
            if char in Word.TEX_CONTROL_CHAR or char in Word.TEX_CONTROL_PUNC:
                length += 1
                name.append(char)
                source.update()
                tp = Word.TYPE_CPUNC
                break
        if char.islower() or char.isupper():
            length+=1
            name.append(char)
            source.update()
            continue
        else:
            break
            # 序列结束
    name = ''.join(name)

    return Word(tp, length, name, pos)










def split(src): # 对于src 进行词法分解
    logging.info('************ split ************')
    source = Source(src)
    words = Words(src)
    poscounter = PostionCounter(source, words) # 统计当前的行号, 位置信息

    text_pos = poscounter.get_pos()

    while True:
        char =  source.getchar()
        if not char : break
        # start

        if char in Word.TEX_CHAR or char == '\\':
            # 处理普通文本
            if text_pos:
                l = poscounter.get_pos()[2] - text_pos[2]
                w = Word(Word.TYPE_TEXT,  l, 'text', text_pos)
                words.append(w)
                text_pos = None

            if char in Word.TEX_CHAR:# 特殊字符

                w = Word(Word.TYPE_PUNC, 1, char, poscounter.get_pos())
                words.append(w)
                poscounter.update(char)  # 更新行
                source.update()


            elif char == '\\': # 控制序列
                w = get_control(source, poscounter.get_pos())
                words.append(w)


                # 处理结束的char 不是序列的, 再次进入循环
                continue
        else:
            if text_pos == None:
                text_pos = poscounter.get_pos()

            poscounter.update(char)  # 更新行
            source.update()
    return words

def show_word_details(words):
    for w in words:

        name = w.name()
        if w.type == Word.TYPE_PUNC:
            if name == '\n':
                name = '\\n'
            elif name == ' ':
                name = 'space'

        print "%s|%s,%s" % (name, w.pos[0], w.pos[1])

class Words(object):# 对于进行词法分析的结果进行包装, 是语法分析中的依赖
    def __init__(self, source, start = 0, end = None, words = None):
        self.source = source # 记录source, 不是source 对象
        if not words:
            words = []
        self.words = words

        self.start = start
        if not end: end = len(self.words)
        self.end = end

        self.pos = start
    def show(self):
        return (self.start, self.end, self.pos)

    def getall(self, name):# 得到所有名为name 的word 在Words中的index
        sn_index = []
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == name:
                sn_index.append(index + self.pos - self.start)
        return sn_index

    def getpos(self):
        return self.pos

    def initpos(self, pos):
        self.pos = pos


    def reinit(self):
        self.pos = self.start

    def append(self, w):
        self.words.append(w)
        self.end += 1

    def getcontext(self, word):
        # 依据word 的pos 与length 得到对应的source
        pos = word.pos[2]
        length = word.len
        return self.source[pos: pos + length]

    def get_context_between(self, w1, w2): # 得到两个word 中间的context, 开区间
        s = w1.pos[2] + w1.len
        e = w2.pos[2]
        return self.source[s: e]

    def findnesting(self, name, nesting, inside = True): # 可以嵌套
        # 如果开启了nesting, 那么对于
        logging.debug('find:ws:%s', self.show())
        if inside:
            level = 0
        else:
            level = 1
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == nesting:
                level += 1
            if w.name() == name:
                if level > 1:
                    level -= 1
                    continue

                pos = self.pos + index
                ws = self.slice(self.pos - self.start, pos - self.start + 1)
                self.pos = pos + 1
                return ws
        else:
            w = self.words[self.pos]
            msg = "NOT FOUND:%s from %s, %s" % (name, w.pos[0], w.pos[1])
            raise Exception(msg)

    def find(self, name, nesting = False): # nesting是不是可以嵌套
        # 如果开启了nesting, 那么对于
        logging.debug('find:ws:%s', self.show())
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == name:
                pos = self.pos + index
                ws = self.slice(self.pos - self.start, pos - self.start + 1)
                self.pos = pos + 1
                return ws
        else:
            w = self.words[self.pos]
            msg = "NOT FOUND:%s from %s, %s" % (name, w.pos[0], w.pos[1])
            raise Exception(msg)

    def find_same(self, name):
        end = False
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() != name:
                pos = self.pos + index
                break
        else:
            end = True
            pos = self.pos + index  + 1

        ws = self.slice(self.pos - self.start, pos - self.start)
        self.pos = pos
        return (ws, end)
    def sliceto(self, end):
        if end:
            if end < 0:
                end = self.end + end
            else:
                end = self.start + end
        else:
            end = self.end

        start = self.pos

        return Words(self.source, words = self.words, start= start, end = end)


    def slice(self, start, end=None):
        if end:
            if end < 0:
                end = self.end + end
            else:
                end = self.start + end
        else:
            end = self.end

        start = self.start + start

        return Words(self.source, words = self.words, start= start, end = end)

    def getword(self):
        if self.pos < self.start or self.pos >= self.end:
            return None
        return self.words[self.pos]

    def getword_byindex(self, index):
        if index < 0:
            index = self.end + index
        else:
            index = self.start + index

        if index >= self.end or index < self.start:
            return None
        #print self.pos, ' ', self.end, ' ', self.start, len(self.words)
        return self.words[index]

    def update(self):
        self.pos += 1

    def back(self): # 使用要注意
        self.pos -= 1

    def __len__(self):
        return self.end - self.start

if __name__ == "__main__":
    pass

