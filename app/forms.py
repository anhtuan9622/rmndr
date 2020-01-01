from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from app.models import User

#setup login forms
class LoginForm(FlaskForm):
    user_email = EmailField('email', validators=[DataRequired()])
    user_password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me?')
    submit = SubmitField('let me in')

#setup register forms
class RegisterForm(FlaskForm):
    user_email = EmailField('email', validators=[DataRequired(), Email()])
    user_password = PasswordField('password', validators=[DataRequired()])
    user_password2 = PasswordField('repeat password', validators=[DataRequired(), EqualTo('user_password', message='passwords do not match')])
    submit = SubmitField('sign me up')
    
    #function validate email
    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user is not None:
            raise ValidationError('this email is already registered')

#setup forgot password forms
class ForgotPasswordForm(FlaskForm):
    user_email = EmailField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('reset me')

#setup password reset forms
class ResetPasswordForm(FlaskForm):
    user_password = PasswordField('password', validators=[DataRequired()])
    user_password2 = PasswordField('repeat password', validators=[DataRequired(), EqualTo('user_password', message='passwords do not match')])
    submit = SubmitField('set me')

#setup input forms
class TaskForm(FlaskForm):
    task_name = StringField('task', validators=[DataRequired(), Length(max=128)])
    task_due = DateTimeField('due date', format='%Y-%m-%d %H:%M')
    task_remind = DateTimeField('remind on', format='%Y-%m-%d %H:%M')
    create = SubmitField('set me')
    delete = SubmitField('erase me')
    edit = SubmitField('edit me')