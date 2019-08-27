#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    server_status.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-18 13:26
"""
import configs
from cache import rdb
from service.ext import db
from model.mongo import db as mongodb


def get_redis_info():
    watch_keys = [
        'run_id', 'redis_version', 'uptime_in_seconds', 'role'
    ]
    try:
        info = rdb.info()
        status = {'status': 1}
        for k in watch_keys:
            status[k] = info[k]
    except Exception as err:
        return {'status': 0, 'error': str(err)}
    return status


def get_mongodb_info():
    watch_keys = [
        'version', 'uptime', 'connections', 'ok'
    ]
    try:
        info = mongodb.command('serverStatus')
        status = {'status': 1}
        for k in watch_keys:
            status[k] = info[k]
    except Exception as err:
        return {'status': 0, 'error': str(err)}
    return status


def get_db_info():
    try:
        db.session.execute('SELECT 1')
        status = {'status': 1}
    except Exception as err:
        return {'status': 0, 'error': str(err)}
    return status


def srv_check_application_available():
    service = [
        (get_redis_info, 'redis down'),
        (get_mongodb_info, 'mongodb down'),
        (get_db_info, 'mysql down')
    ]
    for func, err in service:
        r = func()
        if not r['status']:
            return False, err

    return True, 'ok'


def srv_application_data():
    data = {
        'application': configs.project,
        'redis': get_redis_info(),
        'mongodb': get_mongodb_info(),
        'mysql': get_db_info()
    }
    return data
