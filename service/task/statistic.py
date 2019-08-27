#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    statistic.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-17 00:12
"""
import os
import re
import logging
from urllib.parse import parse_qs
from collections import defaultdict
from datetime import datetime, timedelta

from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

import configs
from configs.celery_configs import celery_app
from model.mongo.paste_statistic import PasteStatistic

IP_PATTERN = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
TIME_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')
URI_PATTERN = re.compile(r'\/paste\?u=\w+')


def merge_dict(src_counter, dst_counter):
    for k, v in dst_counter.items():
        if k in src_counter:
            src_counter[k] += v
        else:
            src_counter[k] = v


def get_begin_end_time(datetime_object):
    begin_time = datetime_object.replace(
        hour=0, minute=0, second=0, microsecond=0
    ).strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime_object.replace(
        hour=23, minute=0, second=0, microsecond=0
    ).strftime("%Y-%m-%d %H:%M:%S")
    return begin_time, end_time


def fetch_access_logs(log_dir):
    logs = os.listdir(log_dir)
    abs_logs = [os.path.join(log_dir, l) for l in logs]
    return abs_logs


def extra_visited_data(line):
    data = dict()
    m = IP_PATTERN.search(line)
    if m:
        data['ip'] = m.group()
    m = TIME_PATTERN.search(line)
    if m:
        data['time'] = m.group()
    m = URI_PATTERN.search(line)
    if m:
        data['uri'] = m.group()

    return data


def aggregate_uri_visited_count(log, target_date=None):
    if target_date is None:
        target_date = datetime.utcnow() - timedelta(days=1)
    else:
        target_date = datetime.strptime(target_date, '%Y-%m-%d')

    begin_time, end_time = get_begin_end_time(target_date)
    uri_counter = defaultdict(int)
    with open(log, 'r') as reader:
        for line in reader:
            data = extra_visited_data(line)
            visited_time = data.get('time')
            if not visited_time:
                continue
            if visited_time < begin_time or visited_time > end_time:
                continue
            uri = data.get('uri')
            if not uri:
                continue

            query = uri.split("?")[-1]
            params = parse_qs(query)
            uid = params['u'][0]
            uri_counter[uid] += 1

    return target_date, uri_counter


@celery_app.task
def run_daily_statistic_pv_task(stat_day=None, log_dir=None):
    if log_dir is None:
        log_dir = configs.log['log_dir']

    logs = fetch_access_logs(log_dir)
    pv_counter = dict()

    process_date = None
    for log in logs:
        process_date, counter = aggregate_uri_visited_count(log, stat_day)
        merge_dict(pv_counter, counter)

    if not process_date:
        logging.info("No log to process")
        return

    month = process_date.strftime("%Y-%m")
    requests = []
    for u, c in pv_counter.items():
        doc = UpdateOne(
            {
                PasteStatistic.Field.month: month,
                PasteStatistic.Field.short_url: u
            },
            {
                "$inc": {
                    PasteStatistic.Field.hit_count: c
                },
                "$set": {
                    PasteStatistic.Field.update_time: datetime.utcnow()
                },
                "$setOnInsert": {
                    PasteStatistic.Field._id: PasteStatistic.generate_id(),
                    PasteStatistic.Field.create_time: datetime.utcnow(),
                    PasteStatistic.Field.short_url: u,
                    PasteStatistic.Field.month: month
                }
            },
            upsert=True
        )
        requests.append(doc)

    if requests:
        try:
            PasteStatistic.p_col.bulk_write(requests)
        except BulkWriteError as err:
            logging.error(err, exc_info=True)
            return 0

    logging.info("更新 %s 页面成功" % len(pv_counter))
