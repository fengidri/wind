# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-02 08:34:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import pyvim
import vim

def ctag(filename):
    cmd = "ctags --sort=no -f - -n --fields=-lzf %s" % filename
    f = os.popen(cmd)
    pyvim.log.debug("cmd: %s", cmd)

    tags = {}

    for line in f.readlines():
        tmp = line.split()

        keyword        = tmp[0] #tag name
        tp             = tmp[3] # 类型如 f
        linenu         = int(tmp[2][0: -2])# 行号, ctag 输出如: 114;"

        if len(tmp) > 4:
            cls = tmp[4]

        elif tp == 'f':
            cls = 'function'

        elif tp == 'v':
            cls = 'varg'
        else:
            continue

        ms = tags.get(cls)

        if ms:
            ms.append((keyword, linenu, tp))
        else:
            tags[cls] = [(keyword, linenu, tp)]
    return tags



import frainui
class CTagList(object):
    def __init__(self):
        self.tags = {}
        self.b = vim.current.buffer

        self.listwin = frainui.LIST("TagList", self.getcls)
        self.listwin.show()
        self.listwin.refresh()


    def ctag(self):
        name = self.b.name
        tags = self.tags.get(name)
        if not tags:
            tags = ctag(name)
            self.tags[name] = tags

        return tags

    def getcls(self, Node):
        for k in self.ctag():
            n = frainui.Node(k, k, self.fr_list_cls)
            Node.append(n)

    def fr_list_cls(self, Node):
        tags = self.ctag()[Node.ctx]
        for tag in tags:
            if tag[2] == 'f':
                name = '\\red%s\end' % tag[0]
            elif tag[2] == 'm':
                name = '\\blue%s\end' % tag[0]
            elif tag[2] == 'v':
                name = '\\green%s\end' % tag[0]
            else:
                name = tag[0]
            n = frainui.Leaf(name, tag[1], self.fr_tag_pos)
            Node.append(n)

    def fr_tag_pos(self, leaf):
        vim.current.window.cursor = (leaf.ctx, 0)

TAGLIST = None

@pyvim.cmd()
def TagList():
    global TAGLIST
    if not TAGLIST:
        TAGLIST = CTagList()



if __name__ == "__main__":

    pass

