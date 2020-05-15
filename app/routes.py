from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from app.models import User
from werkzeug.urls import url_parse
from app.auth import make_auth_url, check_state, get_tokens, open_auth_url
from app.api_calls import get_username, get_all_playlists
import sys
import time
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        auth_url = make_auth_url()
        open_auth_url(auth_url)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/callback')
def callback():
    state = request.args.get('state', '')
    if not check_state(state):
        abort(403)
    token_info = get_tokens(request.args.get('code'))
    user_id = get_username(token_info['access_token'])
    expiration_time = int(token_info['expires_in']) + int(time.time())
    session['id'] = user_id
    session.permanent = True
    if User.query.get(user_id) is None:
        new_user = User(id=user_id,
                        access_token=token_info['access_token'],
                        refresh_token=token_info['refresh_token'],
                        expiration_time=expiration_time)
        db.session.add(new_user)
    else:
        session['id'] = user_id
        updating_user = User.query.get(user_id)
        updating_user.access_token = token_info['access_token']
        updating_user.refresh_token = token_info['refresh_token']
        updating_user.expiration_time = expiration_time
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/shuffler', methods=['GET', 'POST'])
def shuffler():
    playlists  = g.current_user.get_user_playlists()
    return render_template('shuffler.html', playlists=playlists)


@app.route('/temp')
def test_func():
    get_all_playlists()
    return redirect(url_for('index'))
