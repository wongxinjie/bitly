#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    echo.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-19 17:11
"""
from flask import request

from internal_api import internal_api as api


@api.route('/echo', methods=['GET', 'POST', 'PUT'])
def api_echo():
    args = request.args.to_dict()
    data = request.form.to_dict()
    json = request.get_json()
    return {'message': 'ok', 'args': args, 'data': data, 'json': json}
