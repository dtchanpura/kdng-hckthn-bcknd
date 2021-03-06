import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '\xdc8\xdb\xd2\x9d\xbe?\n#vo\xe4\xb2\x17/v\x1c\x02\xb1\x11\xba\x9c\\t'

TMP_FOLDER = 'tmp/'
if os.environ.get('DEBUG') == "TRUE":
    DEBUG = True
else:
    DEBUG = False
VERSION = os.environ.get('APP_VERSION', 0)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
