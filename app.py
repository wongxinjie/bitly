#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    app.py
    ~~~~~~~~~~~~~~~~~~~~


    :author: wongxinjie
    :date created: 2019-08-12 23:47
"""
import logging
from flask import Flask, jsonify

import configs
from service.session import Session
from service.ext import (
    db,
    migrate,
    limiter,
    env_dump,
    health_check,
    login_manager,
)
from error import BitlyError


def create_app(app_conf=None):
    if app_conf is None:
        app_conf = configs.FlaskAppConfig

    app = Flask(__name__)
    app.config.from_object(app_conf)
    app.host = app_conf.HOST
    app.port = app_conf.PORT

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    @app.before_request
    def before_request():
        pass

    @app.after_request
    def after_request(response):
        return response

    @app.teardown_request
    def teardown_request(response):
        # TODO: implement after request here, close database connection etc.
        return response

    return app


def register_extensions(app):
    """
    在这里统一注册app extensions
    :param app:
    :return:
    """
    db.init_app(app)
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        return Session.load_user(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": 401, "message": "unauthorized"}), 401

    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 是否开启状态检查
    if configs.health_check['open']:
        add_app_health_check(app)

    limiter.init_app(app)


def register_blueprints(app):
    if configs.api['toggle_api']:
        from api import api
        app.register_blueprint(api, url_prefix="/api")
    if configs.api['toggle_internal_api']:
        from internal_api import internal_api
        app.register_blueprint(internal_api, url_prefix="/internal-api")


def register_error_handlers(app):

    @app.errorhandler(Exception)
    def error_handler(e):
        logging.error(e, exc_info=True)
        if isinstance(e, BitlyError):
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
        else:
            if app.debug:
                message = repr(e)
            else:
                message = '服务不可用'
            response = jsonify({"message": message, "status_code": BitlyError.status_code})
            response.status_code = BitlyError.status_code
        return response

    @app.errorhandler(422)
    def handle_processable_entity(err):
        data = getattr(err, 'data')
        errors = data['messages']
        return jsonify({
            'stat': 1,
            'msg': errors,
            'err': 10
        }), 400

    @app.errorhandler(401)
    def handler_401(e):
        rsp = {
            'message': 'Unauthorized',
            'error': 401
        }
        if isinstance(e.description, int):
            rsp['error'] = e.description
        elif isinstance(e.description, dict):
            rsp.update(e.description)
        return jsonify(**rsp), 401

    @app.errorhandler(400)
    def handler_400(e):
        rsp = {
            'message': 'Bad Request',
            'error': 400
        }
        if isinstance(e.description, int):
            rsp['error'] = e.description
        elif isinstance(e.description, dict):
            rsp.update(e.description)
        return jsonify(**rsp), 400

    @app.errorhandler(403)
    def handler_403(e):
        rsp = {
            'message': 'Forbidden',
            'error': 403
        }
        if isinstance(e.description, int):
            rsp['error'] = e.description
        elif isinstance(e.description, dict):
            rsp.update(e.description)
        return jsonify(**rsp), 403

    @app.errorhandler(404)
    def handler_404(e):
        rsp = {
            'message': 'Not Found',
            'error': 404
        }
        if isinstance(e.description, int):
            rsp['error'] = e.description
        elif isinstance(e.description, dict):
            rsp.update(e.description)
        return jsonify(**rsp), 404

    @app.errorhandler(429)
    def handle_limit_rate(e):
        rsp = {
            'message': 'Too Many Request',
            'error': 429
        }
        return jsonify(**rsp), 429


def register_shell_context(app):
    pass


def add_app_health_check(app):
    from service.server_status import srv_check_application_available
    from service.server_status import srv_application_data

    health_check.init_app(app, configs.health_check['path'])
    env_dump.init_app(app, configs.health_check['env_path'])
    health_check.add_check(srv_check_application_available)
    env_dump.add_section("app", srv_application_data)
