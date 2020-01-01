from flask import render_template, url_for
from flask_mail import Message
from app import app, mail, celery
from app.models import User, Task

#function send welcome email
@celery.task
def send_email_welcome(user_id):
    user = User.query.get_or_404(user_id)
    with app.app_context():
        msg = Message('welcome to rmndr v1.0', sender=app.config['ADMINS'][0], recipients=[user.user_email])
        msg.html = render_template('emails/email_welcome.html')
        mail.send(msg)

#function send mail reset password
@celery.task
def send_email_reset_password(user_id):
    user = User.query.get_or_404(user_id)
    token = user.get_reset_password_token()
    with app.app_context():
        msg = Message('reset password - rmndr v1.0', sender=app.config['ADMINS'][0], recipients=[user.user_email])
        msg.html = render_template('emails/email_reset_password.html', user=user, token=token)
        mail.send(msg)

#function send mail reminder
@celery.task
def send_email_reminder(task_id):
    task = Task.query.get_or_404(task_id)
    user = User.query.get_or_404(task.user_id)
    with app.app_context():
        msg = Message('your task reminder - rmndr v1.0', sender=app.config['ADMINS'][0], recipients=[user.user_email])
        msg.html = render_template('emails/email_reminder.html', task=task)
        mail.send(msg)