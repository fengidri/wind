# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-21 13:40:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

Objects = {}

class Object(object):
    __CB = {}
    def FREventEmit(self, event):
        cbs = self.__CB.get(event)
        if not cbs:
            return

        for cb in cbs:
            fun = cb[0]
            args = cb[1]
            if args:
                return fun(self, *args)
            else:
                return fun(self)

    def FREventBind(self, event, fun, arg = None):
        funs = self.__CB.get(event)
        if funs:
            funs.append((fun, arg))
        else:
            self.__CB[event] = [(fun, arg)]

    def FRRegister(self, name):
        Objects[name] = self



if __name__ == "__main__":
    pass

