from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt

#config 'user' db table
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(320), nullable=False, unique=True, index=True)
    user_password_hash = db.Column(db.String(128))
    task = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"['user_id': '{self.user_id}', 'user_email': '{self.user_email}']"

    def set_password(self, password):
            self.user_password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.user_password_hash, password)
    
    def get_id(self):
           return (self.user_id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#config 'task' db table
class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), nullable=False, index=True)
    task_due = db.Column(db.DateTime(timezone=True), index=True)
    task_remind = db.Column(db.DateTime(timezone=True), index=True)
    task_sent = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return f"['task_id': '{self.task_id}', 'task_name': '{self.task_name}', 'task_due': '{self.task_due}', 'task_remind': '{self.task_remind}', 'task_sent': '{self.task_sent}']"