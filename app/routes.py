from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse
from spotipy import util
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    scopes = 'playlist-modify-public user-library-read playlist-modify-private'
    form = LoginForm()
    if form.validate_on_submit():
        user_token = util.prompt_for_user_token(form.username.data,
                                                scopes,
                                                os.environ.get('SPOTIPY_CLIENT_ID'),
                                                os.environ.get('SPOTIPY_SECRET_ID'),
                                                os.environ.get('SPOTIPY_REDIRECT_URI'))
        if user_token:
            flash(user_token)
            # login_user(user_token, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))