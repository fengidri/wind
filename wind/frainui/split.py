# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-06-16 10:08:16
#    email     :   fengidri@yeah.net
#    version   :   1.0.1



import Buffer
class Search(Buffer.BF, SearchWIN, BufferEvent, EnterEvent):
    def __init__(self, lines, name='search'):
        Buffer.BF.__init__(self)
        self.lines = lines
        self.match_line = None
        self.match_id = []
        self.nos = [] # the show lines index in the origin list
        self.name = name

        self.edit_win = vim.current.window

        self.FRRegister(name)

        self.BFFt       = "frainuiSearch"
        self.BFName     = "Search"
        self.BFCreate()

        from enter import EnterLine
        self.enter = EnterLine(self, 0, "Search:")
        self.enter.FREventBind("Enter-Active", self.enter_active)
        self.enter.FREventBind("Enter-Change", self.enter_change)

        self.FREventBind("OP-Active", self.option_active)
        self.FREventBind("OP-Quit", self.quit)

        self.BFSetImFocus(self.enter)

        self.show_list(lines)



