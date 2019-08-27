#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    user.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 00:28
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from service.ext import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True)
    mobile = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(512))
    is_deleted = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, default=datetime.utcnow())

    __table_args__ = (
        db.Index("username_idx", username),
        db.Index("email_idx", email),
        db.Index("mobile_idx", mobile),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "mobile": self.mobile,
            "is_deleted": self.is_deleted,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat(),
        }

    @property
    def raw_password(self):
        raise AttributeError("password was not accessible")

    @raw_password.setter
    def raw_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class LoginUser(UserMixin):
    def __init__(self, **kwargs):
        UserMixin.__init__(self)
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __contains__(self, key):
        return key in self.__dict__

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

