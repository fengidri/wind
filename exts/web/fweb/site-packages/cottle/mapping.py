# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-20 10:53:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from http_wsgi import HTTPError, HTTPResponse
import re
import types
from py23k import *
import session


# 用于增加到用户类的方法



################################################################################
class Mapping(object):
    def load(self, mapping):
        self.mapping = []

        for pat, handle in mapping:
            pat = '^%s$' % pat
            self.mapping.append((pat, handle()))
            #handle = self.init_handle(handle, fvars)
            #if not handle: continue
            #self.mapping.append((pat, handle))

    #def init_handle(self, handle, fvars):
    #    if handle is None:
    #        return
    #    elif isinstance(handle, (types.ClassType, type)): # is_class
    #        return self.__init_handle(handle)
    #    elif isinstance(f, basestring):
    #        cls = None
    #        if '.' in f:
    #            mod, cls = f.rsplit('.', 1)
    #            mod = __import__(mod, None, None, [''])
    #            cls = getattr(mod, cls)
    #        else:
    #            cls = self.fvars.get(f)
    #        if cls:
    #            return self.__init_handle(cls)
    #        return
    #    else:
    #        return

    #def __init_handle(self, cls):
    #    return cls()


    def match(self, path):
        for pat, handle in self.mapping:
            #暂时不支持application
            #webpy中动态修改回调字符串的方式也不支持
            match = re.search(pat, path)
            if match:
                return handle, match.groups()
        return None, []

    def session(self, handle, request, response):
        if not handle.check_session:
            handle.session = None
            return

        ses = session.get_session(request)
        if not ses:
            ses = session.SessionCls()
            if ses.login(request):
                ses.save(response)
            else:
                raise HTTPError(401, "login error")
        handle.session = ses
        #对会话权限进行检查.
        if handle.pam:
            handle.session.check(handle.pam)

    def call(self, handle, args, request, response):
        if handle is None:
            raise HTTPError(404, "Not Found")

        meth = request.method
        if meth == 'HEAD' and not hasattr(handle, meth):
            meth = 'GET'
        if not hasattr(handle, meth):
            raise HTTPError(404, "Not Found Handle:%s" % meth)


        handle.params = args
        handle.request  = request
        handle.response = response
        self.session(handle, request, response)

        if handle.Before():
            res = getattr(handle, meth)()

        handle.After()

        if not isinstance(res, basestring):
            response.content_type = "application/json"
            try:
                return json_dumps(res)
            except:
                return res
        return res

if __name__ == "__main__":
    pass

