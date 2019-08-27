#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    test_srv_account.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 17:22
"""
from model.sql.user import User
from service.account import srv_create_account


def test_create_account(app):
    mobile = '13612444229'
    email = 'user1@bitly.com'
    password = '123456'

    User.query.filter(
        (User.mobile == mobile) | (User.email == email)
    ).delete()

    err_code = srv_create_account(password, mobile=mobile)
    assert err_code == 0
    user = User.query.filter_by(mobile=mobile).first()
    assert user is not None and user.to_dict()['mobile'] == mobile

    err_code = srv_create_account(password, mobile=mobile)
    assert err_code == 1

    err_code = srv_create_account(password, email=email)
    assert err_code == 0
    user = User.query.filter_by(email=email).first()
    assert user is not None and user.to_dict()['email'] == email
    err_code = srv_create_account(password, email=email)
    assert err_code == 1

    User.query.filter(
        (User.mobile == mobile) | (User.email == email)
    ).delete()
