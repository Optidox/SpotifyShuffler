from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField


class LoginForm(FlaskForm):
    submit = SubmitField('Log in with Spotify')


class ShufflerForm(FlaskForm):
    checkboxes = SelectMultipleField('Select Playlists', choices=[])
    submit = SubmitField('Shuffle')
