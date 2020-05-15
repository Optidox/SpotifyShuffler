from flask_wtf import FlaskForm
from wtforms import SubmitField


class LoginForm(FlaskForm):
    submit = SubmitField('Log in with Spotify')