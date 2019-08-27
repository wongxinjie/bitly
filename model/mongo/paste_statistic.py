#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste_track.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:41
"""
from bson import ObjectId
from pymongo import ReadPreference, DESCENDING
from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from model.mongo import db


class PasteStatistic:
    """
    页面访问统计

    * `_id` (str)
    * `short_url` (str) - 短链
    * `month` (str) - 统计月份
    * `hit_count` (int) - 访问次数
    * `create_time` (utc datetime)
    * `update_time` (utc datetime)
    """

    COL_NAME = 'paste_statistic'

    p_col = Collection(
        db, COL_NAME, read_preference=ReadPreference.PRIMARY_PREFERRED
    )
    s_col = Collection(
        db, COL_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    class Field:
        _id = '_id'
        short_url = 'short_url'
        month = 'month'
        hit_count = 'hit_count'
        create_time = 'create_time'
        update_time = 'update_time'

    try:
        p_col.create_index([(Field.month, DESCENDING), (Field.short_url, DESCENDING)],
                           unique=False, sparse=False)
    except OperationFailure as err:
        print(err)

    @staticmethod
    def generate_id():
        return str(ObjectId())
