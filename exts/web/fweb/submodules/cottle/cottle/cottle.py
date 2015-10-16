# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 14:36:17
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import logging
import plugins
from bottle import Bottle
from http_wsgi import request
from http_wsgi import response
import os
from mapping import Mapping
from Error import RouteReset
from http_wsgi import HTTPError
from py23k import _stderr, _e#why

from static import static_file

# http
from http_wsgi import HTTPResponse
from traceback import format_exc, print_exc

class Cottle(Bottle):
    plugins_path = 'plugin'
    URLS = []
    PLUGINS  = []
    def __init__(self, opts = {}):
        Bottle.__init__(self)

        self.mapping = Mapping()  # mapping to handle call add by feng
        self.pre_static = opts.get('pre_static') or "/static"
        self.path_static = opts.get('path_static') or ''
        self.plugins_path = opts.get('plugin')


        logging.info('**************** start cottle ******************')

        self.load_plugin()
        self.logurls()
        self.mapping.load(self.URLS)

    def groups(self, urls):
        i = 0
        t = []
        while i < len(urls):
            t.append((urls[i], urls[i+1]))
            i = i + 2
        return t


    def load_plugin(self):
        ps = plugins.load(self.plugins_path)
        for mode, name, urls in ps.values():
            self.mode_init(mode, name, urls)

    def mode_init(self, mode, name, urls):
        for url, fun in self.groups(urls):
            if url.startswith('/'):
                url = '/%s%s' % (name, url)
            else:
                url = os.path.join('/', name, url)


            if isinstance(fun, basestring):
                if not hasattr(mode, fun):
                    logging.error('plugin %s not hasattr [%s]' % (mode, fun))
                    continue
                fun = getattr(mode, fun)

            self.URLS.append((url,fun))
        self.PLUGINS.append((name,mode))

    def logurls(self):
        l = 0
        for u,c in self.URLS:
            if len(u) > l:
                l = len(u)

        lines = ['']
        for u,c in self.URLS:
            lines.append("%s  ===>  %s" % (u.ljust(l),c))
        logging.info('\n'.join(lines))

    def _handle(self, environ):
        path = environ['bottle.raw_path'] = environ['PATH_INFO']
        try:
            environ['bottle.app'] = self

            request.bind(environ)
            response.bind()



            if self.path_static and path.startswith(self.pre_static):
                path = path[len(self.pre_static):]
                return static_file(path, self.path_static)

            handle, args = self.mapping.match(path)
            if handle:
                environ['route.handle'] = handle
                environ['bottle.route'] = handle
                environ['route.url_args'] = args
                res  = self.mapping.call(handle, args, request, response)
                return res
            else:
                raise HTTPError(404)

        except HTTPResponse:
            return _e()
        except RouteReset:
            route.reset()
            return self._handle(environ)
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            if not self.catchall: raise
            stacktrace = format_exc()
            environ['wsgi.errors'].write(stacktrace)
            return HTTPError(500, "Internal Server Error", _e(), stacktrace)

    def run(self, config = None):
        from ctrl import run
        if not config:
            from config import config
            config = config()

        run(self, config)



if __name__ == "__main__":
    pass

