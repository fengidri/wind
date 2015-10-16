# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-01-08 16:53:42
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import time
import uuid
__SESSION = {}
__KEY = 'cottlekey'
__SECRET = 'cottlesecret'

#对于session 做如下的假定
#1. 超时与没有找到对应的cookie做相同的处理.  调用login方法
#2. 在找到session后会做调用check做权限检查
#3. 
class session(object):
    def __init__(self):
        self.timestamp = time.time()
        while True:
            sesid = uuid.uuid1()
            if sesid in __SESSION:
                continue
            break
        self.sesid = sesid

    def check(self, pam):
        pass#用户自己实现对于pam 进行检查的方法
            # 参数pam 是handle 的属性
    def login(self, request):
        pass
    def save(self, reponse):
        reponse.set_cookie(__KEY, self.sesid, secret = __SECRET)
        __SESSION[self.sesid]= self
    
def get_session(request):
    return request.get_cookie(__KEY, __SECRET)

SessionCls = session

if __name__ == "__main__":
    pass

