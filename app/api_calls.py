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
import sys


# Adapted from Spotipy (client.Spotify._auth_headers)
def _auth_header(access_token):
    return {"Authorization": "Bearer {0}".format(access_token)}


def _get_access_token():
    return


def get_username(*args):
    if args:
        auth_header = _auth_header(args[0])
    else:
        auth_header = _auth_header(_get_access_token())

    response = requests.get("https://api.spotify.com/v1/me", headers=auth_header)
    user_info = response.json()
    return user_info['id']

