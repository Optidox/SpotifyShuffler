from flask import render_template, flash, redirect, url_for, request, abort, session, g
from app import app, db
from app.models import User
from werkzeug.urls import url_parse
from app.auth import make_auth_url, check_state, get_tokens, open_auth_url
from app.api_calls import get_username, get_all_playlists, create_shuffler_playlist, make_shuffled_playlist
import sys
import time
from app.webforms import LoginForm, ShufflerForm


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
    if g.current_user.shuffler_playlist is None:
        create_shuffler_playlist()
    get_all_playlists()

    playlists = g.current_user.get_user_playlists()
    form = ShufflerForm()
    form.checkboxes.choices = [(playlist.name, playlist.name) for playlist in playlists]
    if form.validate_on_submit():
        selected_playlists = [playlist for playlist in playlists if playlist.name in form.checkboxes.data]
        print(selected_playlists, file=sys.stderr)
        make_shuffled_playlist(selected_playlists)
    return render_template('shuffler.html', form=form)
