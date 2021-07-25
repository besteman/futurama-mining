import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or
        'sqlite:///' + os.path.join(basedir, 'instance/flaskr.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
