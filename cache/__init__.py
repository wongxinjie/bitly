#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:29
"""
from redis import StrictRedis

import configs

rdb = StrictRedis(
    host=configs.redis['host'],
    port=configs.redis['port'],
    db=configs.redis['db']
)


class Cache:

    def __init__(self, backend=rdb):
        self.backend = backend

    def set(self, key, value, ex=None, px=None, nx=None, xx=None):
        self.backend.set(key, value, ex, px, nx, xx)

    def get(self, key):
        v = self.backend.get(key)
        if v:
            return v.decode('utf-8')

    def delete(self, key):
        self.backend.delete(key)


cache = Cache(rdb)
