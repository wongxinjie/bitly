#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    account.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 16:59
"""
import uuid
import logging

from service.ext import db
from model.sql.user import User


def srv_create_account(password, email=None, mobile=None):
    """
    :param password:
    :param email:
    :param mobile:
    :return:
    """
    if email is not None:
        count = User.query.filter_by(email=email).count()
        if count:
            return 1

    if mobile is not None:
        count = User.query.filter_by(mobile=mobile).count()
        if count:
            return 1

    username = str(uuid.uuid4()).split('-')[0]
    user = User()
    user.username = username
    user.raw_password = password
    if email:
        user.email = email
    if mobile:
        user.mobile = mobile

    db.session.add(user)
    try:
        db.session.commit()
    except Exception as err:
        logging.error(err, exc_info=True)
        db.session.rollback()
        return -1

    return 0


def srv_get_account_via_email(email):
    return User.query.filter_by(email=email).first()


def srv_get_account_via_mobile(mobile):
    return User.query.filter_by(mobile=mobile).first()
