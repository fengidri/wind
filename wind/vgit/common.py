# -*- coding:utf-8 -*-

import subprocess
from . import output

def run(cmd):
    p = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE, stderr =
            subprocess.STDOUT, text = True)

    if p.stdout:
        output.buf.extend(p.stdout.split('\n'))
