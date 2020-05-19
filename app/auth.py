from urllib.parse import urlencode
import os
from uuid import uuid4
from flask import session, g
import base64
import six
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import webbrowser
import logging
import time
from app import db


# Code adapted from Spotipy (oauth2._make_authorization_headers)
def _make_auth_headers():
    auth_header = base64.b64encode(six.text_type(os.environ.get('SPOTIFY_CLIENT_ID')
                                                 + ':' + os.environ.get('SPOTIFY_CLIENT_SECRET')).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}


def _refresh_token():
    headers = _make_auth_headers()
    payload = {'grant_type': 'refresh_token',
               'refresh_token': g.current_user.refresh_token}

    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    token_json = response.json()
    g.current_user.access_token = token_json['access_token']
    g.current_user.expiration_time = int(token_json['expires_in']) + int(time.time())
    db.session.commit()


def make_auth_url():
    state = str(uuid4())
    session['state_hash'] = generate_password_hash(state, 'sha256')
    params = {
        'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
        'scope': 'playlist-modify-private playlist-modify-public playlist-read-private user-library-read',
        'redirect_uri': os.environ.get('SPOTIFY_REDIRECT_URI'),
        'state': state,
        'response_type': 'code'
    }

    url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
    return url


# Code adapted from Spotipy (oauth2._open_auth_url)
def open_auth_url(auth_url):
    logger = logging.getLogger(__name__)
    try:
        webbrowser.open(auth_url)
        logger.info("Opened %s in your browser", auth_url)
    except webbrowser.Error:
        logger.error("Please navigate here: %s", auth_url)


def check_state(state):
    state_hash = session['state_hash']
    session.pop('state_hash')
    return check_password_hash(state_hash, state)


def get_tokens(code):
    headers = _make_auth_headers()
    payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': os.environ.get('SPOTIFY_REDIRECT_URI')}

    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    token_json = response.json()

    return {'access_token': token_json['access_token'],
            'refresh_token': token_json['refresh_token'],
            'expires_in': token_json['expires_in']}


def check_token():
    if g.current_user.expiration_time < int(time.time()):
        _refresh_token()
