from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from jinja2 import Environment, PackageLoader
# from flask.ext.login import LoginManager
import os

app = Flask(__name__)
app.config.from_object('config')

# lm = LoginManager()
# lm.init_app(app)
db = SQLAlchemy(app)

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/bot.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('bot startup')

if os.environ.get('HEROKU') is not None:
    import logging

    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('bot startup')

from flaskapp import views
