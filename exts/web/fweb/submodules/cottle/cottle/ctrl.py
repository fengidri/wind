# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-15 09:51:10
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


def run(app, config):
    #kargs  = config.get("server_kargs")
    server = config.get("server")

    print("Listening on http://%s:%d/" % (server.host, server.port))
    print("Hit Ctrl-C to quit.\n\n")

    server.run(app)


if __name__ == "__main__":
    pass

