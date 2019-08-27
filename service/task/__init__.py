#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:28
"""
from app import create_app

_app = create_app()
ctx = _app.app_context()
ctx.push()
