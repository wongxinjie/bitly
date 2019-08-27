#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    echo.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-19 17:12
"""
import configs
from service.internal_http_api import BaseClient


class EchoApi(BaseClient):

    def __init__(self, host, salt):
        super().__init__(host, salt)

    def echo(self, params=None):
        url = '%s/internal-api/echo' % self.host
        resp = self.request.get(url, params)
        return resp.to_dict()

    def post_echo(self, params=None, data=None, json=None):
        url = '%s/internal-api/echo' % self.host
        resp = self.request.post(url, params, data, json)
        return resp.to_dict()


echo_api = EchoApi('http://127.0.0.1:6000', configs.api['internal_salt'])
