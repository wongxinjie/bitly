import os
import logging.config
from logging import DEBUG, INFO


import yaml

yaml_f = open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs.yaml'),
    'r', encoding='utf8'
)
config = yaml.safe_load(yaml_f)


class FlaskAppConfig:
    app_config = config.pop('app')
    HOST = app_config['host']
    PORT = app_config['port']
    DEBUG = app_config['debug']
    SECRET_KEY = app_config['secret_key']
    SESSION_COOKIE_NAME = 'xkitSessionId'
    SESSION_COOKIE_DOMAIN = app_config['session_cookie_domain']
    REMEMBER_COOKIE_DOMAIN = app_config['remember_cookie_domain']

    mysql_config = config.pop('mysql')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
        user=mysql_config['user'],
        password=mysql_config['password'],
        host=mysql_config['host'],
        port=mysql_config['port'],
        db=mysql_config['db']
    )
    SQLALCHEMY_ECHO = mysql_config['echo']
    # SQLALCHEMY_POOL_SIZE = mysql_config['pool_size']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


globals().update(config)

DEBUG = FlaskAppConfig.DEBUG
if DEBUG:
    logging_level = DEBUG
else:
    logging_level = INFO


conf = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d #: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging_level,
            'formatter': 'basic',
        },
        'default': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': logging_level,
            'formatter': 'basic',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(config['log']['log_dir'], 'default.log')
        },
        'access': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': logging_level,
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(config['log']['log_dir'], 'access.log')
        },
    },
    'loggers': {
        '': {
            'level': logging_level,
            'handlers': ['console', 'default'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'wsgi': {
            'level': logging_level,
            'handlers': ['access', 'console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'service': {
            'level': logging_level,
            'handlers': ['console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'client': {
            'level': logging_level,
            'handlers': ['console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        }
    },
}

logging.config.dictConfig(conf)
