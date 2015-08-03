# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 16:19:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from nodes import Section, node_tree
import logging

SPLITER = ['\section', '\subsection', '\subsubsection']
SPLITERCALL = [Section, Section, Section]
MAXLEVEL = 2

class ParSection(object):

    def __init__(self, ws, Level, hide = False):
        if Level == 0:
            logging.info('')

        self.msg = 'ParSection:     level: %s %s' % (Level, ws.show())
        logging.info(self.msg)
        self.section = None
        self.Paragraph = None
        self.subParagraph = None
        if not hide:
            self.section = SPLITERCALL[Level](ws)

        if Level >= MAXLEVEL:
            logging.info('TEXT Paragraph: level: %s %s', Level, ws.show())
            self.subParagraph = node_tree(ws)
        else:
            self.Paragraph = SplitParagraph(ws, Level + 1)

    def html(self):
        #h = '\n<!-- %s -->\n' % self.msg
        h = ''
        if self.section:
            h += self.section.html()

        if self.Paragraph:
            return h + self.Paragraph.html()
        else:
            return "%s<p>%s</p>\n" % (h ,self.subParagraph.html())

    def md(self):
        h = ''
        if self.section:
            h += self.section.md()

        if self.Paragraph:
            return h + self.Paragraph.md()
        else:
            return "%s\n%s\n\n" % (h ,self.subParagraph.md())






class SplitParagraph(list):
    def __init__(self, ws, level): # sn: section name

        sn = SPLITER[level]
        sn_index = ws.getall(sn)

        logging.info('SplitParagraph: level: %s %s', level, ws.show())
        logging.debug("SplitParagraph: Sections:%s", sn_index)

        if not sn_index:
            self.append(ParSection(ws, level, hide = True))
            return


        if sn_index[0] != 0:
            _ws = ws.sliceto(sn_index[0])
            self.append(ParSection(_ws, level, hide = True))

        index = 0
        while True:
            if index >= len(sn_index) -1:
                break

            s = sn_index[index]
            index += 1
            e = sn_index[index]

            _ws = ws.slice(s, e)
            self.append(ParSection(_ws, level))

        _ws = ws.slice(sn_index[-1])
        self.append(ParSection(_ws, level))

    def html(self):
        h = [n.html() for n in self]
        return ''.join(h)

    def md(self):
        h = [n.md() for n in self]
        return ''.join(h)



if __name__ == "__main__":
    pass

