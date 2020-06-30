from flask import render_template, redirect, url_for, request, abort, session, g, flash
from app import app, db
from app.models import User
from app.auth import make_auth_url, check_state, get_tokens
from app.api_calls import get_username, get_all_playlists, make_shuffled_playlist
import time
from app.webforms import ShufflerForm


@app.route('/')
@app.route('/index')
def index():
    try:
        return render_template('index.html', title='Home', user=g.current_user)
    except AttributeError:
        return render_template('index.html', title='Home', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(make_auth_url())

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
    if not hasattr(g, 'current_user'):
        flash("Please log in with Spotify before using Shuffler")
        return redirect(url_for('index'))

    get_all_playlists()
    playlists = g.current_user.get_user_playlists()
    shuffler_form = ShufflerForm()
    shuffler_form.playlists.choices = [(playlist.name, playlist.name) for playlist in playlists]
    if shuffler_form.validate_on_submit():
        selected_playlists = [playlist for playlist in playlists if playlist.name in shuffler_form.playlists.data]
        make_shuffled_playlist(selected_playlists)
    return render_template('shuffler.html', shuffler_form=shuffler_form, user=g.current_user)


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect(url_for('index'))
