from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from flask import Flask
import lib.log as log
import logging
from config import config, APP_NAME

Logger = logging.getLogger(APP_NAME)

db = SQLAlchemy()

def initialize_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,resources={r"":{"origins":""}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    log.setup_logging(config[config_name])

    initialize_db(app)

    from app.Music.views import music_bp as music_router
    app.register_blueprint(music_router, url_prefix='/music')

    from app.User.views import user_bp as user_router
    app.register_blueprint(user_router, url_prefix='/user')

    return app
