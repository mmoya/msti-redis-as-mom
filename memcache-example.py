#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import memcache
import time

mc = memcache.Client(['localhost:11211'])

def expensive_hello(s):
    time.sleep(2)
    return 'Hello %s!' % s

def cache_hello():
    key = 'hello'

    value = mc.get(key)
    if value is None:
        value = expensive_hello('world')
        mc.set(key, value)

    return value

value = cache_hello()
print(value)
