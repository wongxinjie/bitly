#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    paste.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-13 23:00
"""
import logging
from datetime import datetime, timedelta

from service.ext import db
from model.sql.paste import Paste
from model.mongo.paste_content import PasteContent
from service.shorten import generate_short_url


def srv_create_paste(
        ip, content, expiration=None, user_id=None, visible_range=None,

):
    doc_id = PasteContent.create(content)
    retry = 3
    short_url = None
    while retry:
        short_url = generate_short_url(ip, content)
        count = Paste.query.filter_by(short_url=short_url).count()
        if not count:
            break
        retry -= 1

    # 生成不成功
    if not short_url:
        PasteContent.delete(doc_id)
        return

    paste = Paste(short_url=short_url, paste_path=doc_id)
    if user_id is not None:
        paste.user_id = user_id
    if expiration is not None:
        paste.expiration_in_minutes = expiration
        paste.expire_time = datetime.utcnow() + timedelta(minutes=expiration)
    if visible_range is not None:
        paste.visible_range = visible_range

    db.session.add(paste)
    try:
        db.session.commit()
    except Exception as err:
        logging.error(err, exc_info=True)
        db.session.rollback()
        PasteContent.delete(doc_id)

    return short_url


def srv_get_short_url_content(short_url, user_id=None):
    paste = Paste.query.filter_by(short_url=short_url).first()
    if not paste:
        return None

    doc = paste.to_dict()
    visible_range = doc.get('visible_range', Paste.VisibleRange.public)
    if visible_range == Paste.VisibleRange.private:
        paste_user_id = doc['user_id']
        if paste_user_id != user_id:
            return None

    payload = {
        'create_at': doc['create_at'],
        'expiration_in_minutes': doc.get('expiration_in_minutes', 0)
    }
    paste_path = doc['paste_path']
    paste_content = PasteContent.get(paste_path)
    if not paste_content:
        return None
    payload['paste_content'] = paste_content
    return payload


def remove_paste_content(paste_ids):
    r = PasteContent.p_col.delete_many({
        PasteContent.Field._id: {
            "$in": paste_ids
        }
    })
    return r.deleted_count


def srv_delete_expire_paste(process_time=None):
    """
    删除已经设置过期的paste
    :param process_time:
    :return:
    """
    if process_time is None:
        process_time = datetime.utcnow()
    else:
        process_time = datetime.strptime(process_time, '%Y-%m-%d %H:%M:%S')

    rows = Paste.query.filter(
        Paste.expire_time <= process_time
    ).all()
    paste_paths = [r.paste_path for r in rows]

    r = Paste.query.filter(
        Paste.expire_time <= process_time
    ).delete(
        synchronize_session='fetch'
    )
    try:
        db.session.commit()
    except Exception as err:
        logging.error(err, exc_info=True)
    else:
        remove_paste_content(paste_paths)
        logging.info("删除过期Paste共: %s 条" % (str(r)))
