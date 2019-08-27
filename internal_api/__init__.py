#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-18 13:15
"""
from flask import Blueprint

from common.http import check_internal_api_request


internal_api = Blueprint("/internal-api", __name__)


@internal_api.before_request
def api_before_request():
    check_internal_api_request()


from internal_api import (
    echo,
    health_check
)
