# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-30 12:28:04
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import imp
from pyvim import log as logging

class Plugins(object):
    def __init__(self, path):
        self.path = path
        self.hook_init = None

    def loads(self):
        if not os.path.isdir(self.path):
            logging.error("plugin path:[%s] is not dir"%self.path)
            return

        modules = os.listdir(self.path)

        for module in modules:
            if not module.endswith(".py"):
                continue

            module_name = module[0:-3]

            module_path = os.path.join(self.path, module)
            sys_name = module_path.replace('.', '_')
            module_loaded = imp.load_source(sys_name, module_path)
            if self.hook_init:
                self.hook_init(module_name, module_loaded)


if __name__ == "__main__":
    pass

