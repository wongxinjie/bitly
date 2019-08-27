#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 00:17
"""
from flask import Blueprint

api = Blueprint("/api", __name__)

from api import (
    paste,
    account
)
