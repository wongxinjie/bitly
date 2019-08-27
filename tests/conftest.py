#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    conftest.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 15:25
"""
import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()
