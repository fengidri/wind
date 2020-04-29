# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-10 14:09:50
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from http_wsgi import HTTPError, HTTPResponse
from template import template as template
from py23k import *
from static import static_file



class handle(object):
    def __init__(self):
        self.request = None
        self.response = None
        self.check_session = True # 是否进行session 检查
        self.pam = None # 权限要求

    def Before(self):
        return True
    def After(self):
        pass

    @property
    def query(self):
        return self.request.query

    @property
    def forms(self):
        return self.request.forms

    @property
    def path(self):
        return self.request.path

    @property
    def env(self):
        return self.request.environ

    def getcookie(self, key, default=None, secret=None):
        return self.request.get_cookie(key)

    def template(self, *args, **kwargs):
        return template(*args, **kwargs)

    def abort(self, code=500, text='Unknown Error.'):
        """ Aborts execution and causes a HTTP error. """
        raise HTTPError(code, text)

    def redirect(self, url, code=None):
        """ Aborts execution and causes a 303 or 302 redirect, depending on
            the HTTP protocol version. """
        if not code:
            if self.request.get('SERVER_PROTOCOL') == "HTTP/1.1":
                code = 303
            else:
                code = 302

        res = self.response.copy(cls=HTTPResponse)
        res.status = code
        res.body = ""
        res.set_header('Location', urljoin(self.request.url, url))
        raise res

    def cfile(self, filename, root, mimetype='auto', download=False,
            charset='UTF-8'):
        return static_file(filename, root, mimetype, download, charset)

    def set_content_json(self):
        self.response.content_type = "application/json"


if __name__ == "__main__":
    pass

