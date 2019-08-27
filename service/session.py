#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    session.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-16 11:05
"""
import json

from flask_login import current_user

from cache import cache
from model.sql.user import User, LoginUser


def get_user_id():
    if current_user.is_authenticated:
        return current_user.id


class Session:

    @classmethod
    def generate_cache_key(cls, user_id):
        return 'bitly:user:session:{}'.format(user_id)

    @classmethod
    def load_user(cls, user_id):
        key = cls.generate_cache_key(user_id)
        user_data = cache.get(key)
        if user_data:
            user_dict = json.loads(user_data)
            return LoginUser(**user_dict)

        user = User.query.get(user_id)
        if user:
            user_dict = user.to_dict()
            user_data = json.dumps(user_dict)
            cache.set(key, user_data, ex=3600)
            return LoginUser(**user_dict)

    @classmethod
    def purse_cache_user(cls, user_id):
        key = cls.generate_cache_key(user_id)
        cache.delete(key)
