# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-21 13:40:13
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

#    对于 object 进行记录. 一般的 object 要用 name 进行注册
#    Buffer object 使用 vim.buffer 对象进行注册
Objects = {}
import pyvim

class Object(object):
    Buffer = None
    IM     = None # 要处理输入流的对象应该提供这个属性
    def FREventEmit(self, event, *k):
        if not hasattr(self, '_CB_'):
            return

        try:
            cbs = self._CB_.get(self).get(event, [])
        except:
            return

        for cb in cbs:
            cb(self, *k)

    def FREventBind(self, event, cb):
        if not hasattr(self, '_CB_'):
            self._CB_ = {}

        evs = self._CB_.get(self)

        if not evs:
            evs = self._CB_[self] = {}

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

class FRObject(Object):
    def init(self, Buffer=None, IM=None):
        self._Buffer_ = Buffer
        self._IM_     = IM
        self._CB_     = {}

    def FREventEmit(self, event, *k):
        try:
            cbs = self._CB_.get(self).get(event, [])
        except:
            return

        for cb in cbs:
            cb(self, *k)

    def FREventBind(self, event, cb):
        evs = self._CB_.get(self)

        if not evs:
            evs = self._CB_[self] = {}

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
        self._Buffer_.input_focus = self

