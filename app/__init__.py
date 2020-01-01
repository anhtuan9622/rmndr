from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from celery import Celery

#setup app
app = Flask(__name__)

#initialize config
app.config.from_object(Config)

#initialize db sqlalchemy
db = SQLAlchemy(app)

#initialize db migrate
migrate = Migrate(app, db)

#initialize login
login = LoginManager(app)
login.login_view = 'login'
login.login_message = ''

#initialize mail server
mail = Mail(app)

#initialize background task celery
celery = Celery(app.name, broker = app.config['CELERY_BROKER_URL'])

from app import views, models