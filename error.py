#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    error.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 00:22
"""


class BitlyError(Exception):

    status_code = 500

    def __init__(self, message, status_code, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        content = dict(self.payload or ())
        content['message'] = self.message
        content['status_code'] = self.status_code
        content['stat'] = 0
        return content
