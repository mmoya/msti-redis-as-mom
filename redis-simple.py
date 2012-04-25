#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import redis
import time

rd = redis.Redis('localhost')

def expensive_hello(s):
    time.sleep(2)
    return 'Hello %s!' % s

def cache_hello():
    key = 'hello'

    value = rd.get(key)
    if value is None:
        value = expensive_hello('world')
        rd.set(key, value)

    return value

value = cache_hello()
print(value)
