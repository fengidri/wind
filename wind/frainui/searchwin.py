# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 09:30:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import pyvim
def getfiles(path):
    cmd = 'cd {path}; find . {filter} 2>/dev/null'
    fs = [
            " -type d -name '.*' -prune -o ",
            " -type f  ! -name '.*' -and ",
            " -type f  ! -name '*.o' -and ",
            " -type f  ! -name '*.so' ",
            " -print "
            ]
    cmd = cmd.format(path = path, filter = ''.join(fs))
    return os.popen(cmd).readlines()



class SearchWIN(object):
    def __init__(self):
        import Buffer
        import enter
        self.buf = Buffer.Buffer(title = "Search", ft="frainuiSearch")
        self.buf.show()

        self.enter = enter.EnterLine(self.buf, 0, "Search:")
        self.enter.FRInputFocus()
        self.enter.FREventBind("change", self.enter_change)
        #import tree
        #self.tree  = tree.Tree(self.buf, 2, 15)

    def enter_change(self, enter, c):
        pyvim.log.error("enter_change: %s", c)






if __name__ == "__main__":
    pass

