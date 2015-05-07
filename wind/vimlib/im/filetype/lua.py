# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 10:50:50
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import im.imutils
import im.inputers as inputers
import logging
import pyvim
FTS = ['lua']

class code(inputers.IM_Code):
    def cb_dot(self):
        pyvim.feedkeys('.', 'n')


class im_ft(im.imutils.filetype):
    im_ft = FTS
    def __init__(self):
        w = ["CCommentDesc", "CCommentArg", "Constant", "Comment", "String"]
        c = ['*']
        self.im_append(inputers.IM_Path())
        #self.im_append(inputers.IM_Wubi(w))
        self.im_append(code(c))
        self.im_append(inputers.IM_Base())



if __name__ == "__main__":
    pass

