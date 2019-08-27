#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    ext.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-12 23:46
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from healthcheck import HealthCheck, EnvironmentDump

import configs

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
health_check = HealthCheck()
env_dump = EnvironmentDump(
    include_config=False, include_os=False,
    include_process=False, include_python=False
)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=configs.redis['uri'],
    headers_enabled=True
)
