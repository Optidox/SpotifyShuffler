from app import app, db
from app.models import User
from app.auth import check_token
from flask import g, session


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


@app.before_request
def load_current_user():
    if 'id' in session and User.query.get(session['id']) is not None:
        g.current_user = User.query.get(session['id'])
        check_token()
    return None
