from app import app, db, login
from app.models import User, Task

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))