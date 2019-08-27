#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    account.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 16:59
"""
from flask import request
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from api import api
from service.ext import limiter
from service.session import Session
from service.account import srv_create_account
from service.account import srv_get_account_via_email
from model.sql.user import LoginUser
from common.http import abort_400, abort_401


@api.route('/register', methods=['POST'])
@limiter.limit('10/minute')
def api_create_account():
    params = request.get_json()
    email = params.get('email')
    password = params['password']

    # TODO: check mobile and email
    if not email:
        abort_400('email should not be empty')

    err_code = srv_create_account(password, email=email)
    if err_code:
        abort_400('email had been taken', 10)

    return {"ok": 1}


@api.route('/login/password', methods=['POST'])
@limiter.limit('5/minute')
def api_login_via_password():
    params = request.get_json()
    email = params['email']
    password = params['password']

    user = srv_get_account_via_email(email)
    if not user or not user.verify_password(password):
        abort_401('account not exist or password not match')

    user_data = user.to_dict()
    login_user(LoginUser(**user_data))
    return {'error': 0, 'message': 'ok', 'uid': user_data['id']}


@api.route("/logout")
def api_logout():
    user_id = current_user.id
    Session.purse_cache_user(user_id)
    logout_user()
    return {'error': 0, 'message': 'ok'}


@api.route("/ok", methods=['GET'])
@login_required
@limiter.limit('100/minute')
def api_ok():
    return {"name": current_user.username}, 201
