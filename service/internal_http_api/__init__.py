#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-19 10:31
"""
import time
import json
import uuid
import socket
import logging

import requests
import pyhystrix
from requests.exceptions import RequestException

from common.http import signature


class ApiResponse:

    def __init__(self, status_code=200, content=None, error=None):
        self.status_code = status_code
        self.content = content
        self.error = error

    def to_dict(self):
        if isinstance(self.content, dict):
            payload = self.content
        else:
            payload = json.loads(self.content)
        payload['status_code'] = self.status_code
        return payload


class ApiRequest:
    def __init__(self, salt, sign_func, timeout=10):
        self.salt = salt
        self.timeout = timeout
        self.sign_func = sign_func
        self.headers = {'X-Request-Host': socket.gethostname()}

    def do_request(self, method, url, params=None, data=None, json=None, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('allow_redirects', True)

        # 增加时间戳和nonce
        nonce = str(uuid.uuid4()).replace('-', '')
        ts = int(time.time() * 1000)
        if params is None:
            params = {'nonce': nonce, 'ts': ts}
        else:
            params.update({'nonce': nonce, 'ts': ts})

        headers = self.headers
        kw_headers = kwargs.pop('headers', None)
        if kw_headers:
            headers.update(kw_headers)

        sign_value = self.sign_func(self.salt, method, url, params, data, json)
        params.update({'sign': sign_value})

        headers['X-Sign'] = sign_value
        headers['X-Nonce'] = nonce
        try:
            response = requests.request(
                method=method, url=url, params=params, data=data, json=json,
                headers=headers, **kwargs
            )
        except RequestException as err:
            logging.debug(err)
            result = ApiResponse(
                status_code=500,
                content={"message": "Server Error"},
                error=err
            )
        else:
            result = ApiResponse(
                status_code=response.status_code,
                content=response.content
            )
        return result

    def get(self, url, params, headers=None):
        return self.do_request('GET', url, params, headers=headers)

    def post(self, url, params, data=None, json=None, **kwargs):
        return self.do_request('POST', url, params, data, json, **kwargs)

    def put(self, url, params, data=None, json=None, **kwargs):
        return self.do_request('PUT', url, params, data, json, **kwargs)

    def delete(self, url, params, data=None, json=None, **kwargs):
        return self.do_request('DELETE', url, params, data, json, **kwargs)


class BaseClient:

    def __init__(self, host, salt, sign_func=signature):
        """

        :param host: 服务host
        :param salt: 第三方服务salt
        :param sign_func: 签名方法
        """
        self.host = host
        self.salt = salt
        self.sign_func = sign_func
        self.request = ApiRequest(salt, sign_func)
        # 增加断路器ß
        pyhystrix.Init()

