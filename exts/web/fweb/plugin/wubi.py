# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-01-22 12:25:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from cottle import  handle
import wbtree
name = 'wubi'
urls = ('/search', 'search',
        '/setcount', 'setcount')
class search(handle):
    def GET(self):
        patten  = self.query.get('patten')
        return wbtree.wbsearch(patten)

class setcount(handle):
    def GET(self):
        patten  = self.query.get('patten')
        word  = self.query.get('word').decode('utf8')
        wbtree.wbsetcount(patten, word)
        return 'OK'



if __name__ == "__main__":
    pass

