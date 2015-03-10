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
def key_to_feed(key):
    if key in imrc.digits:
        return key

    elif key in imrc.lowerletter:
        return key

    elif key in imrc.upperletter:
        return key

    elif key in imrc.puncs:
        return imrc.puncs.get(key)[1]

    elif key in imrc.mults:
        return imrc.puncs.get(key)[1]
    else:
        logging.error("key:%s is not imrc" % key)

def key_to_see(key):
    if key in imrc.digits:
        return key
    elif key in imrc.lowerletter:
        return key
    elif key in imrc.upperletter:
        return key
    elif key in imrc.puncs:
        return imrc.puncs.get(key)[0]
    elif key in imrc.mults:
        return imrc.puncs.get(key)[0]

def key_feed(key):
    k = key_to_feed(key)
    if k:
        pyvim.feedkeys(k, 'n')


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

