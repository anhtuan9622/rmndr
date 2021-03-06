import os

# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #config server (if running locally)
    # SERVER_NAME = 'localhost:5000'

    #config flask-wtf key
    SECRET_KEY = os.environ.get('SECRET_KEY') or '278a2a34a27d8fc880e4c10e343792a4f0ad52b0a6b5b40b'

    #config SQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://root:admin@127.0.0.1:5432/rmndr'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #config mail server
    DEBUG = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'yourpassword'
    ADMINS = [MAIL_USERNAME]
    
    #config Celery broker
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379'
    CELERY_TIMEZONE	= 'UTC'
