from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db, celery, mail
from app.models import User, Task
from app.forms import TaskForm, LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from app.email import send_email_reset_password, send_email_reminder, send_email_welcome
from flask_mail import Message
from datetime import datetime
from tzlocal import get_localzone
import pytz

#set default task_sent db column to 'false' 
task_sent = 0

#function convert UTC datetime to local for jinja filter
def datetimelocal(value, format="%A, %B %d, %Y at %I:%M %p"):
    # value = pytz.utc.localize(value, is_dst=None)
    local_datetime = value.astimezone(get_localzone())
    return local_datetime.strftime(format)
#declare jinja filter
app.jinja_env.filters['datetimelocal'] = datetimelocal

#function login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(user_email=login_form.user_email.data).first()
        if user is None or not user.check_password(login_form.user_password.data):
            flash('incorrect email or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='log in', login_form=login_form)

#function logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#function register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(user_email=register_form.user_email.data)
        user.set_password(register_form.user_password.data)
        db.session.add(user)
        db.session.commit()
        #send welcome email
        send_email_welcome.apply_async(args=(user.user_id,), countdown=2)
        flash('signed up successfully! you can login now')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', register_form=register_form)

#function forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    forgot_password_form = ForgotPasswordForm()
    if forgot_password_form.validate_on_submit():
        user = User.query.filter_by(user_email=forgot_password_form.user_email.data).first()
        if user:
            send_email_reset_password.apply_async(args=(user.user_id,), countdown=2)
        flash('check your email for the link to reset your password')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', title='forgot password', forgot_password_form=forgot_password_form)

#function reset password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('register'))
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():
        user.set_password(reset_password_form.user_password.data)
        db.session.commit()
        flash('your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='reset password', reset_password_form=reset_password_form)

#function home page
@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        user = current_user
    task = Task.query.filter_by(user_id=current_user.get_id())
    task_form = TaskForm()
    return render_template('index.html', title='home', task=task, task_form=task_form, current_user=current_user)

#function create new task
@app.route('/create_task', methods=['POST'])
def create_task():
    task_form = TaskForm()
    if not task_form.task_name.data:
        flash('please fill task name')
    else:
        #convert local datetime to UTC
        if task_form.task_due.data:
            task_due_local = get_localzone().localize(task_form.task_due.data, is_dst=None)
            task_due_utc = task_due_local.astimezone(pytz.utc)
        else:
            task_due_utc = task_form.task_due.data
        if task_form.task_remind.data:
            task_remind_local = get_localzone().localize(task_form.task_remind.data, is_dst=None)
            task_remind_utc = task_remind_local.astimezone(pytz.utc)
        else:
            task_remind_utc = task_form.task_remind.data
        
        new_task = Task(task_name=task_form.task_name.data, task_due=task_due_utc, task_remind=task_remind_utc, task_sent=task_sent, user_id=current_user.get_id())
        db.session.add(new_task)
        db.session.commit()
        flash('yay! task is created successfully!')

        #check task_remind and send scheduled reminder by email
        if new_task.task_remind:
            if new_task.task_remind < datetime.utcnow().replace(tzinfo=pytz.utc):
                flash('...but task reminder is past')
            else:
                send_email_reminder.apply_async(args=(new_task.task_id,), eta=new_task.task_remind)
                flash('task reminder is also scheduled')
    return redirect(url_for('index'))

#function delete existing task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    current_task = Task.query.get_or_404(task_id)
    if current_task:
        db.session.delete(current_task)
        db.session.commit()
    flash('task is deleted!')
    return redirect(url_for('index'))

#function edit task
@app.route('/edit_task/<int:task_id>', methods=['POST', 'GET'])
def edit_task(task_id):
    task = Task.query.filter_by(user_id=current_user.get_id())
    current_task = Task.query.get_or_404(task_id)
    if current_task.task_due:
        current_task.task_due = current_task.task_due.astimezone(get_localzone())
    if current_task.task_remind:
        current_task.task_remind = current_task.task_remind.astimezone(get_localzone())
    task_form = TaskForm(obj=current_task)
    
    if request.method == 'POST':
        if not task_form.task_name.data:
            flash('task name can\'t be blank')
        else:
            #convert local datetime to UTC
            if task_form.task_due.data:
                task_form.task_due.data = task_form.task_due.data.astimezone(pytz.utc)
            if task_form.task_remind.data:
                task_form.task_remind.data = task_form.task_remind.data.astimezone(pytz.utc)

            task_form.populate_obj(current_task)
            db.session.commit()
            flash('task is edited successfully')

            #check task_remind and send scheduled reminder by email
            if current_task.task_remind:
                if current_task.task_remind < datetime.utcnow().replace(tzinfo=pytz.utc):
                    flash('...but task reminder is past')
                else:
                    send_email_reminder.apply_async(args=(current_task.task_id,), eta=current_task.task_remind)
                    flash('task reminder is also scheduled')

            return redirect(url_for('index'))
    return render_template('edit.html', title='edit', task=task, task_form=task_form)

#function handle error
error_list = [404, 500]
for c in error_list:
    @app.errorhandler(c)
    def page_not_found(e):
        flash('error page not found')
        return redirect(url_for('index'))