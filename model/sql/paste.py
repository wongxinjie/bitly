#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 00:29
"""
from datetime import datetime

from service.ext import db


class Paste(db.Model):

    __tablename__ = "paste"

    id = db.Column(db.BigInteger, primary_key=True)
    short_url = db.Column(db.String(32), nullable=False)
    expiration_in_minutes = db.Column(db.Integer, default=0)
    paste_path = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.BigInteger)
    visible_range = db.Column(db.SmallInteger)
    expire_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    __table_args__ = (
        db.Index("short_url_idx", short_url),
        db.Index("created_at_idx", created_at.desc()),
    )

    class VisibleRange:
        public = 0
        private = 1

    def to_json(self):
        return {
            "id": self.id,
            "short_url": self.short_url,
            "visible_range": self.visible_range,
            "user_id": self.user_id,
            "expiration_in_minutes": self.expiration_in_minutes,
            "paste_path": self.paste_path,
            "create_at": self.created_at.isoformat()
        }
