from flask import Flask, session, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app.models import User
from app.auth import check_token


@app.before_request
def load_current_user():
    if 'id' in session and User.query.get(session['id']) is not None:
        g.current_user = User.query.get(session['id'])
        check_token()
    return None
