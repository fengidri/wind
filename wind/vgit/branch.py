# -*- coding:utf-8 -*-

import os
def branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
