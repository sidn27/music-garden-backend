import os
from information import *

HOME = '/tmp'
HOME = os.environ.get('LOG_HOME') or HOME
LOG_DIR = 'music_garden'
LOG_FILE = 'music_garden.log'
DEBUG_LOG_FILE = 'music_garden_debug.log'
ERROR_LOG_FILE = 'music_garden_error.log'
DB_FILE = 'music_garden_db.log'
PORT = 5000
APP_NAME = 'music_garden'


class Config:
    DEBUG = False
    TESTING = False
    API_TIMEOUT = 5

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    HOME = '/tmp'
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ":" + DB_PASSWORD + '@' + DB_INSTANCE + '/' + DB_DATABASE
    SECRET_KEY = 'a tout le monde'
    TOKEN_SECRET = 'musicgarden'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    HOME = '/var/log/'
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ":" + DB_PASSWORD + '@' + DB_INSTANCE + '/' + DB_DATABASE


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
