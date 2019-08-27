#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    celery.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-16 17:54
"""
from celery import Celery, platforms
from celery.schedules import crontab

from configs import config

platforms.C_FORCE_ROOT = True
project_name = config['project'].get('name', __file__)


celery_app = Celery('%s-celery' % project_name, include=[
    # 在这里导入定义了celery task的模块
    'service.task.paste',
    'service.task.statistic'
])


celery_app.conf.update(
    broker_url=config['celery']['broker'],
    timezone='UTC',
    task_serializer='json',
    result_serializer='json',
    concurrency=2,
    task_acks_late=True,
    ignore_result=True,
    task_store_error_even_if_ignore=True,
    worker_prefetch_multiplier=True,
    event_queue_expires=7200,
    enable_utc=True
)

celery_app.conf.task_routes = {
    # 一个业务模块的一步任务一般放在同一个模块，将任务发送到不同的queue
    # 让不同的worker 处理
    "service.task.paste.*": "paste-job-queue",
    "service.task.statistic.*": "statistic-job-queue"
}

celery_app.conf.beat_schedule = {
    "remove-expire-paste-periodic": {
         "task": "service.task.paste.run_remove_expire_paste_task",
         "schedule": crontab(minute='*/1'),
     },
    "statistic-paste-pv-task": {
        "task": "service.task.statistic.run_daily_statistic_pv_task",
        # "schedule": crontab(hour=1, minute=30)
        'schedule': crontab(minute='*/2'),
    }
}

# 默认使用default队列，如果你将某个task routing到指定的队列，那么任务不会被执行
# celery -A configs.celery_configs worker -l info

# 为worker指定明确的队列，那么worker只会指定这个队列的任务，即使在task列表中会有
# 一大长串的任务
# celery -A configs.celery_configs worker -l -info -Q queue_a

# worker并发，对于一些IO密集型，比如请求接口，可以使用gevent替代默认的并发模型
# celery -A configs.celery_configs  worker -l info -Q queue_a -c 10 -P gevent
