from flask import Flask

from app.config import Config
from app.views import bp


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if config:
        app.config.update(config)
    app.config.from_pyfile("config.py", silent=True)
    app.register_blueprint(bp)
    return app
