from urllib.parse import urlencode
import os
from uuid import uuid4
from flask import session, g
from app.auth import check_token
from app.models import Playlist
from app import db
import base64
import six
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import webbrowser
import logging
import sys


# Adapted from Spotipy (client.Spotify._auth_headers)
def _auth_header(access_token):
    return {"Authorization": "Bearer {0}".format(access_token)}


def _get_access_token():
    check_token()
    return g.current_user.access_token


def get_username(*args):
    if args:
        auth_header = _auth_header(args[0])
    else:
        auth_header = _auth_header(_get_access_token())

    response = requests.get("https://api.spotify.com/v1/me", headers=auth_header)
    user_info = response.json()
    return user_info['id']


def get_all_playlists():
    auth_header = _auth_header(_get_access_token())
    payload = {'limit': '50',
               'offset': 0}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=auth_header, params=payload)
    has_next = True

    while has_next:
        playlists_info = response.json()
        for item in playlists_info['items']:
            playlist_id = item['id']
            playlist_name = item['name']
            new_playlist = Playlist(playlist_id=playlist_id, name=playlist_name, user_id=g.current_user.id)
            db.session.add(new_playlist)
        if playlists_info['next'] is not None:
            response = requests.get(playlists_info['next'], headers=auth_header)
        else:
            has_next = False
    db.session.commit()
