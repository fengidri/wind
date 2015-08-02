# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-30 12:28:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# TODO 试图导入目录. 可以使用修改 __builtin__.__import__ 的方法

import os
import sys
import imp
from pyvim import log as logging
import pyvim

class Plugins(object):
    def __init__(self, path):
        self.path = path
        self.hook_init = None

    def loads(self):
        if not os.path.isdir(self.path):
            logging.error("plugin path:[%s] is not dir"%self.path)
            return

        for module in os.listdir(self.path):
            module_path = os.path.join(self.path, module)
            if os.path.isdir(module_path):
                _module_path = os.path.join(module_path, '__init__.py')
                if not os.path.exists(_module_path):
                    continue
                sys.path.insert(0, module_path)
                self.load_source(_module_path)
            else:
                self.load_source(module_path)


    def load_source(self, path):
        if not path.endswith(".py"):
            return

        sys_name = path.replace('.', '_')

        try:
            module_loaded = imp.load_source(sys_name, path)
        except:
            pyvim.echo("Load [%s] Fail"% path)
            import traceback
            logging.error(traceback.format_exc())

        #if self.hook_init:
        #    self.hook_init(module[0:-3], module_loaded)


if __name__ == "__main__":
    pass

