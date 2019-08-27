#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-14 01:04
"""
from flask import request, jsonify

import configs
from api import api
from service.paste import (
    srv_create_paste,
    srv_get_short_url_content
)
from service.ext import limiter
from service.session import get_user_id
from common.http import abort_400, abort_404


@api.route("/paste", methods=['POST'])
def api_create_paste():
    ip = request.remote_addr
    body = request.get_json()

    paste_content = body.get('paste_content')
    if not paste_content:
        abort_400('content should not be empty')

    expiration = body.get('expiration')
    if expiration:
        if not isinstance(expiration, int):
            expiration = int(expiration)

    user_id = get_user_id()
    if user_id:
        visible_range = body.get('visible_range', 0)
    else:
        visible_range = None

    s_url = srv_create_paste(
        ip, paste_content, expiration, user_id, visible_range
    )
    if not s_url:
        abort_400('could not generate short url for content', 10)

    url = '{}/api/paste?u={}'.format(configs.domain, s_url)
    return {'short_url': url, 'u': s_url}


@api.route("/paste", methods=['GET'])
@limiter.limit('1000/hour;100/minute')
def api_get_paste():
    url = request.args.get('u', '')

    user_id = get_user_id()
    payload = srv_get_short_url_content(url, user_id)
    if not payload:
        abort_404('content not found')

    return jsonify(**payload)


