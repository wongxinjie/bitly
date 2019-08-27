#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    migrate_table.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 23:48
"""
from app import create_app
from service.ext import db


def create_tables():
    app = create_app()
    with app.app_context():
        r = db.create_all()
        db.session.commit()
        print(r)


if __name__ == "__main__":
    create_tables()
