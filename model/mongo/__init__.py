#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    __init__.py.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:23
"""
from pymongo import MongoClient

from configs import config


def open_connection(database, host='localhost:27017', is_auth=False,
                    user='', password='', is_replica=False, replica=''):
    """

    :param database:
    :param host:
    :param is_auth:
    :param user:
    :param password:
    :param is_replica:
    :param replica:
    :return:
    """
    if is_replica:
        url = "mongodb://%s/?replicaSet=%s" % (host, replica)
    else:
        url = host

    client = MongoClient(url, connect=False)
    connection = client[database]
    if is_auth:
        connection.authenticate(user, password)

    return connection


db = open_connection(
    database=config['mongodb']['db'],
    host=config['mongodb']['host'],
    user=config['mongodb']['user'],
    password=config['mongodb']['password'],
    is_replica=config['mongodb']['is_replica'],
    replica=config['mongodb']['replica'],
    is_auth=config['mongodb']['is_auth']
)