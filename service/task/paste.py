#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-16 17:59
"""
from configs.celery_configs import celery_app
from service.paste import srv_delete_expire_paste


@celery_app.task
def run_remove_expire_paste_task():
    srv_delete_expire_paste()
