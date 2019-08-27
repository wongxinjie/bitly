#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste_content.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 01:31
"""
from bson import ObjectId
from pymongo import ReadPreference, DESCENDING
from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from model.mongo import db


class PasteContent:
    """
    短连接对应的内容

    * `_id` (str)
    * `pasted_id` (int) - 内容对应的记录
    * `content` (string) - 原始内容
    """

    COL_NAME = 'paste_content'

    p_col = Collection(
        db, COL_NAME, read_preference=ReadPreference.PRIMARY_PREFERRED
    )
    s_col = Collection(
        db, COL_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    class Field:
        _id = '_id'
        content = 'content'

    try:
        p_col.create_index([(Field.content, DESCENDING)],
                           unique=False, sparse=False)
    except OperationFailure as err:
        print(err)

    @staticmethod
    def generate_id():
        return str(ObjectId())

    @classmethod
    def create(cls, content):
        doc_id = cls.generate_id()
        doc = {
            cls.Field._id: doc_id,
            cls.Field.content: content
        }
        cls.p_col.insert_one(doc)
        return doc_id

    @classmethod
    def delete(cls, doc_id):
        cls.p_col.delete_one({cls.Field._id: doc_id})

    @classmethod
    def get(cls, doc_id):
        row = cls.s_col.find_one({cls.Field._id: doc_id})
        if row:
            return row[cls.Field.content]
