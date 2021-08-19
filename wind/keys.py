# -*- coding:utf-8 -*-

keys_name_map = {}

def set_key(name, *value):
    name = "KEY_%s" % name

    s = 0
    for a in value:
        s = s * 1000 + a

    v = s

    globals()[name] = v
    keys_name_map[v] = name

def set_keys(s, e = None):
    if not e:
        e = s

    i = ord(s)
    while i <= ord(e):
        set_key(chr(i), i)
        i += 1

set_keys('0', '9')
set_keys('a', 'z')
set_keys('A', 'Z')
set_keys('A', 'Z')

set_key("ENTER", ord('\r'))
set_key("SPACE", ord(' '))
set_key("TAB", ord('\t'))
set_key("ESC", 0x1B)

set_key("DEL",   128, 107, 98)

set_key("UP",    128, 107, 117)
set_key("DOWN",  128, 107, 100)
set_key("LEFT",  128, 107, 108)
set_key("RIGHT", 128, 107, 114)

set_key("MOUSE_DOWN",    128, 253, 76)
set_key("MOUSE_UP",      128, 253, 75)

set_key("MOUSE_PRESS",   128, 253, 44)
set_key("MOUSE_RELEASE", 128, 253, 46)

set_key("MOUSE_DB_PRESS",   128, 252, 32, 128, 253, 44)
set_key("MOUSE_DB_RELEASE", 128, 252, 32, 128, 253, 46)

def convert(keys):
    s = 0
    for a in keys:
        s = s * 1000 + a

    return s

def key_name(key):
    return keys_name_map.get(key)

def char(key):
    if key < 256:
        return chr(key)

