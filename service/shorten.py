#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    shorten.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:51
"""
import time
import hashlib

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
URL_LENGTH = 7


def gen_random_hash(ip, text):
    now = int(time.time() * 1000)
    text = '{}{}{}'.format(ip, text, now)
    return hashlib.md5(text.encode()).hexdigest()


def base62_sum(s):
    base = len(BASE62)
    size = len(s)

    num = 0
    for idx, c in enumerate(s):
        power = size - idx - 1
        num += BASE62.index(c) * (base ** power)

    return num


def base62_encode(s):
    num = base62_sum(s)

    if num == 0:
        return BASE62[0]

    digits = []
    while num:
        idx = num % 62
        digits.append(BASE62[idx])
        num = int(num / 62)
    digits.reverse()
    return ''.join(digits)


def generate_short_url(ip, text):
    s = gen_random_hash(ip, text)
    encode_text = base62_encode(s)
    return encode_text[:URL_LENGTH]





