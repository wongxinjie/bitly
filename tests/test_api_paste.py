#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    test_api_paste.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-15 12:09
"""
from urllib.parse import urlencode

import pytest

from service.ext import db
from service.account import srv_create_account
from model.sql.user import User
from model.sql.paste import Paste

EMAIL1 = 'test1@email.com'
PASSWORD1 = '123456'
EMAIL2 = 'test2@email.com'
PASSWORD2 = '1234567'


def assert_create_paste_success(client, data):
    url = '/api/paste'
    response = client.post(url, json=data)
    data = response.get_json()
    assert response.status_code == 200
    assert 'short_url' in data
    assert 'u' in data

    return data


def assert_get_paste_success(client, u):
    url = '/api/paste'
    args = {'u': u}
    url = '%s?%s' % (url, urlencode(args))
    response = client.get(url)
    assert response.status_code == 200

    data = response.get_json()
    assert 'paste_content' in data
    return data


def assert_get_paste_not_found(client, u):
    url = '/api/paste'
    args = {'u': u}
    url = '%s?%s' % (url, urlencode(args))
    response = client.get(url)
    assert response.status_code == 404


def assert_paste_exists(short_url, user_id=None):
    paste = Paste.query.filter_by(short_url=short_url).first()
    assert paste is not None
    if user_id:
        assert paste.to_dict().get('user_id') == user_id


def test_api_paste_un_login(client):
    content = 'http://bitly.com'

    payload = {'paste_content': content, 'expiration': 5}
    data = assert_create_paste_success(client, payload)

    u = data['u']
    data = assert_get_paste_success(client, u)
    assert data['paste_content'] == content
    assert 'expiration_in_minutes' in data
    assert data['expiration_in_minutes'] == 5


@pytest.fixture(scope='function')
def login_user(app):
    User.query.filter(User.email.in_([EMAIL1, EMAIL1])).delete(synchronize_session='fetch')
    db.session.commit()
    srv_create_account(PASSWORD1, email=EMAIL1)
    srv_create_account(PASSWORD2, email=EMAIL2)
    yield

    User.query.filter(User.email.in_([EMAIL1, EMAIL2])).delete(synchronize_session='fetch')
    db.session.commit()


def login(client, email, password):
    return client.post('/api/login/password', json={
        'email': email, 'password': password
    })


def logout(client):
    return client.get('/api/logout')


def test_api_paste_login(client, login_user):
    urls_to_clean_up = []

    response = login(client, EMAIL1, PASSWORD1)
    assert response.status_code == 200

    json_data = response.get_json()
    user_id = json_data.get('uid')
    assert user_id is not None

    test_case_1 = {'paste_content': 'test-case-1'}
    data = assert_create_paste_success(client, test_case_1)
    u = data['u']
    urls_to_clean_up.append(u)
    assert_paste_exists(u, user_id)
    assert_get_paste_success(client, u)

    test_case_2 = {'paste_content': 'test-case-2', 'visible_range': 1}
    data = assert_create_paste_success(client, test_case_2)
    u = data['u']
    urls_to_clean_up.append(u)
    assert_paste_exists(u, user_id)
    assert_get_paste_success(client, u)

    logout(client)

    assert_get_paste_success(client, urls_to_clean_up[0])
    assert_get_paste_not_found(client, urls_to_clean_up[1])

    login(client, EMAIL2, PASSWORD2)
    assert_get_paste_success(client, urls_to_clean_up[0])
    assert_get_paste_not_found(client, urls_to_clean_up[1])

    Paste.query.filter(Paste.short_url.in_(urls_to_clean_up)).delete(
        synchronize_session='fetch'
    )
    db.session.commit()
