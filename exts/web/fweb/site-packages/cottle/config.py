# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-15 09:50:40
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from adapter import server_names, ServerAdapter

class _config(object):
    def get_server(self, server):
        host = self.get('host')
        port = self.get('port')

        if server in server_names:
            server = server_names.get(server)

        if isinstance(server, type):
            return server(host=host, port=port)


class config(_config):
    server = 'wsgiref'
    host   = "127.0.0.1"
    port   = 8080
    def __init__(self):
        pass

    def get(self, arg):
        if arg == 'server':
            return self.get_server(self.server)


        if hasattr(self, arg):
            return getattr(self, arg)
        else:
            return None



if __name__ == "__main__":
    pass

