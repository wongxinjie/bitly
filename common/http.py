#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    http.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 21:39
"""
import time

from flask import abort, request

import configs
from common.auth import signature


def abort_400(message, code=400):
    payload = {
        'error': code,
        'message': message
    }
    abort(400, payload)


def abort_401(message, code=401):
    payload = {
        'error': code,
        'message': message
    }
    abort(401, payload)


def abort_403(message, code=403):
    payload = {
        'error': code,
        'message': message
    }
    abort(403, payload)


def abort_404(message, code=404):
    payload = {
        'error': code,
        'message': message
    }
    abort(404, payload)


def check_internal_api_request():
    sign_value = request.headers.get('X-Sign')
    if not sign_value:
        sign_value = request.args.get('sign')
        if not sign_value:
            abort_401('no sign found', 1000)

    params = request.args.to_dict()
    params.pop('sign', None)

    if request.method in ['POST', 'PUT']:
        data = request.form.to_dict()
        json = request.get_json()
    else:
        data = None
        json = None

    cal_sign = signature(
        configs.api['internal_salt'], request.method, request.url, params, data, json
    )
    if cal_sign != sign_value:
        abort_401('no valid sign', 1001)

    sign_timestamp = params.get('ts')
    if not sign_timestamp or not sign_timestamp.isdigit():
        abort_401('no request timestamp found', 1002)

    sign_timestamp = int(sign_timestamp)
    current_ts = int(time.time() * 1000)
    if current_ts - sign_timestamp > 50000:
        return abort_401('request timestamp expired', 1003)
