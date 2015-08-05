# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-21 13:40:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

Objects = {}
EVENT_BIND_TYPE_NORMAL = 0
EVENT_BIND_TYPE_CHAIN = 1

class Object(object):
    __CB = {}
    Buffer = None
    IM     = None
    def FREventEmit(self, event, *k):
        evs = self.__CB.get(self)
        if not evs:
            return

        cbs = evs.get(event)
        if not cbs:
            return

        for cb in cbs:
            fun  = cb["fun"]
            args = cb["arg"]
            tp   = cb["type"]
            if tp == EVENT_BIND_TYPE_CHAIN:
                fun.FREventEmit(args)
            else:
                fun(self, *k)

    def FREventBind(self, event, fun, arg = None):
        # 绑定对于事件 event 的处理函数
        """

        """
        tp = EVENT_BIND_TYPE_NORMAL
        if isinstance(fun, Object):
            tp = EVENT_BIND_TYPE_NORMAL

        cb = {"fun": fun, "arg": arg, "type": tp}
        evs = self.__CB.get(self)

        if not evs:
            evs = self.__CB[self] = {}

        funs = evs.get(event)
        if funs:
            funs.append(cb)
        else:
            evs[event] = [cb]


    def FRRegister(self, name):
        Objects[name] = self

    def FRInputFocus(self):
        self.Buffer.input_focus = self

    def FRIM(self, tp, key):
        if self.IM:
            attr_nm = "im_%s" % tp
            getattr(self.IM, attr_nm)(key)
            self.im_post()

    def im_post(self):
        pass




if __name__ == "__main__":
    pass

