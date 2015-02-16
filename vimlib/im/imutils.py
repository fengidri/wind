# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-02-16 10:57:41
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import pyvim
import imrc
import logging
def key_all():
    keys = []
    for k in imrc.digits + imrc.lowerletter + imrc.upperletter:
        keys.append((k,k))
    for k,n in imrc.puncs.items() + imrc.mults.items():
        keys.append((n[0], k))
    return keys

def key_feed(key):
    if key in imrc.digits:
        pyvim.feedkeys(key, 'n')

    elif key in imrc.lowerletter:
        pyvim.feedkeys(key, 'n')

    elif key in imrc.upperletter:
        pyvim.feedkeys(key, 'n')

    elif key in imrc.puncs:
        pyvim.feedkeys(imrc.puncs.get(key)[1], 'n')

    elif key in imrc.mults:
        pyvim.feedkeys(imrc.mults.get(key)[1], 'n')
    else:
        logging.error("key:%s is not imrc" % key)

class filetype(object):
    def im_append(self, im):
        
        if not hasattr(self, '_ims'):
            self._ims = []
        self._ims.append(im)
        logging.error(self._ims)

    def im(self, key):
        logging.debug(self._ims)
        for m in self._ims:
            logging.debug("filetype: inputer: %s" % m)
            if m.im(key):
                return True

            



if __name__ == "__main__":
    pass

