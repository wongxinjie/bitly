#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
    bitly.py
    ~~~~~~~~~~~~~~~~~~~~
 
 
    :author: wongxinjie
    :date created: 2019-08-12 22:18
"""
import logging
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from app import create_app


def run():
    app = create_app()
    http_server = WSGIServer((app.host, app.port), app, log=logging.getLogger('wsgi'))

    if app.debug:
        from werkzeug.serving import run_with_reloader

        @run_with_reloader
        def run_server():
            http_server.serve_forever()
    else:
        http_server.serve_forever()


if __name__ == "__main__":
    run()

