# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-21 13:45:08
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import im.imutils
import im.inputers as inputers
import logging
FTS = ['frainsearch']

logging.error('load frainui')

class im_ft(im.imutils.filetype):
    im_ft = FTS
    def __init__(self):
        self.im_append(inputers.IM_Stream())



if __name__ == "__main__":
    pass

