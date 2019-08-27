#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    auth.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-19 14:26
"""
import hmac
import hashlib
from urllib.parse import urlparse


def strip_url(url):
    result = urlparse(url)
    return '{}://{}{}'.format(result.scheme, result.netloc, result.path)


def signature(salt, method, url, params=None, data=None, json=None):
    payload = dict()
    if params:
        payload.update({k: v for k, v in params.items() if v})
    if data:
        payload.update({k: v for k, v in data.items() if v})
    if json:
        payload.update({k: v for k, v in json.items() if v})

    sorted_params = sorted(payload.items(), key=lambda x: x[0])
    data = '&'.join(['='.join(map(lambda x: str(x), p)) for p in sorted_params])
    method = method.upper()
    url = strip_url(url)
    context = 'method={method}&url={url}&data={data}'.format(
        method=method, url=url, data=data
    )

    md5 = hmac.new(salt.encode('utf-8'), context.encode('utf-8'), hashlib.sha256)
    sign = md5.hexdigest()
    return sign

