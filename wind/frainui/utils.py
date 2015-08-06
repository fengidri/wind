# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-21 13:40:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

#    对于 object 进行记录. 一般的 object 要用 name 进行注册
#    Buffer object 使用 vim.buffer 对象进行注册
Objects = {}

class Object(object):
    __CB = {}
    Buffer = None
    IM     = None # 要处理输入流的对象应该提供这个属性
    def FREventEmit(self, event, *k):
        try:
            cbs = Object.__CB.get(self).get(event, [])
        except:
            return

        for cb in cbs:
            cb(self, *k)

    def FREventBind(self, event, cb):
        evs = self.__CB.get(self)

        if not evs:
            evs = self.__CB[self] = {}

        funs = evs.get(event)
        if funs:
            funs.append(cb)
        else:
            evs[event] = [cb]


    def FRRegister(self, name):
        # let all
        Objects[name] = self

    def FRInputFocus(self):
        # set the focus in the is self
        self.Buffer.input_focus = self



if __name__ == "__main__":
    pass

