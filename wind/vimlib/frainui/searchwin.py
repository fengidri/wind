# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 09:30:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

class SearchWIN(object):
    def createwin(self):
        vim.command("10new")
        vim.command("set ft=frainsearch")
        w = vim.current.window
        b = vim.current.buffer
        b[0] = '>>'
        return (w, b)

class SearchApi(object):
    def getfiles(self, path):
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

class SearchInputWin(object):# 过滤条件的输入
    def __init__(self, w, b, select):
        self.w = w
        self.b = b
        self.select = select

    def input(self, key):
        pass

class SearchSelectWin(object):
    def __init__(self, w, b):
        self.w = w
        self.b = b

    def input(self, key):
        pass

class SearchInput(object):# 处理输入的父类
    INPUTMODE=True
    def __init__(self, w, b):
        self.selectwin = SearchSelectWin(w, b)
        self.inputwin= SearchInputWin(w, b, self.selectwin)

    def input(self, key):
        """
            `模式' 有 inputwin 和 selectwin 两种.
            输入是 <tab> 时进行模式切换
            依据 mode 调用不同的类进行处理.
        """
        if key == '<tab>':
            if self.INPUTMODE:
                self.INPUTMODE = False
                self.selectwin.enter()
            else:
                self.INPUTMODE = True
                self.inputwin.enter()
        else:
            if self.INPUTMODE:
                self.inputwin.input(key)
            else:
                self.selectwin.input(key)


class Search(object):
    def input(self, key):
        pass


if __name__ == "__main__":
    pass

