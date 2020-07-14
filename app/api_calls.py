from flask import g
from app.auth import check_token
from app.models import Playlist
from app import app, db
import requests
from random import shuffle
import json
from itertools import chain
from datetime import datetime


# Adapted from Spotipy (client.Spotify._auth_headers)
def _auth_header(access_token):
    return {"Authorization": "Bearer {0}".format(access_token)}


def _get_access_token():
    check_token()
    return g.current_user.access_token


def _get_playlist_track_uris(playlist_id):
    app.logger.error(playlist_id)
    auth_header = _auth_header(_get_access_token())
    response = requests.get('https://api.spotify.com/v1/playlists/%s/tracks' % playlist_id, headers=auth_header)
    playlist_info = response.json()
    tracks = []
    has_next = True
    while has_next:
        for item in playlist_info['items']:
            if item['is_local'] is False and 'track' in item and item['track'] is not None and 'uri' in item['track']:
                track_uri = item['track']['uri']
                tracks.append(track_uri)
        if playlist_info['next'] is not None:
            response = requests.get(playlist_info['next'], headers=auth_header)
            playlist_info = response.json()
        else:
            has_next = False
    return tracks


def _clear_shuffler_playlist():
    auth_header = _auth_header(_get_access_token())
    shuffler_playlist_id = g.current_user.shuffler_playlist
    response = requests.delete('https://api.spotify.com/v1/playlists/%s/followers' % shuffler_playlist_id, 
                               headers=auth_header)


def get_username(*args):
    if args:
        auth_header = _auth_header(args[0])
    else:
        auth_header = _auth_header(_get_access_token())

    response = requests.get('https://api.spotify.com/v1/me', headers=auth_header)
    user_info = response.json()
    return user_info['id']


def get_all_playlists():
    auth_header = _auth_header(_get_access_token())
    payload = {'limit': '50',
               'offset': 0}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=auth_header, params=payload)
    playlists_info = response.json()
    has_next = True
    playlists_in_db = Playlist.query.filter_by(user_id=g.current_user.id).all()

    for playlist in playlists_in_db:
        playlist.deleted = True

    while has_next:
        for item in playlists_info['items']:
            playlist_id = item['id']
            playlist_name = item['name']
            current_playlist = Playlist.query.filter_by(user_id=g.current_user.id, playlist_id=playlist_id).first()
            if current_playlist is None:
                new_playlist = Playlist(playlist_id=playlist_id,
                                        name=playlist_name,
                                        user_id=g.current_user.id,
                                        deleted=False)
                db.session.add(new_playlist)
            else:
                current_playlist.name = playlist_name
                current_playlist.deleted = False
        if playlists_info['next'] is not None:
            response = requests.get(playlists_info['next'], headers=auth_header)
            playlists_info = response.json()
        else:
            has_next = False

    db.session.commit()
    for playlist in playlists_in_db:
        if playlist.deleted is True:
            db.session.delete(playlist)
    db.session.commit()


def _create_shuffler_playlist(playlists):
    _clear_shuffler_playlist()
    auth_header = _auth_header(_get_access_token())
    auth_header['Content-Type'] = 'application/json'
    creation_time = datetime.now()
    payload = {'name': 'Shuffler',
            'description': f'Playlist created by Shuffler on {creation_time.strftime("%Y-%m-%d")} at {creation_time.strftime("%H:%M:%S")} UTC from these playlists: {", ".join([playlist.name for playlist in playlists])}',
               'public': True}
    response = requests.post('https://api.spotify.com/v1/users/%s/playlists' % g.current_user.id,
                             headers=auth_header,
                             data=json.dumps(payload))
    playlist_info = response.json()
    g.current_user.shuffler_playlist = playlist_info['id']
    db.session.commit()


def make_shuffled_playlist(playlists):
    _create_shuffler_playlist(playlists)
    auth_header = _auth_header(_get_access_token())
    auth_header['Content-Type'] = 'application/json'
    shuffler_playlist_id = g.current_user.shuffler_playlist
    tracks = list(chain(*[_get_playlist_track_uris(playlist.playlist_id) for playlist in playlists]))
    shuffle(tracks)

    track_uris = {'uris': []}
    for i in range(1, len(tracks) + 1):
        track_uris['uris'].append(tracks[i-1])
        if i % 100 is 0:
            requests.post('https://api.spotify.com/v1/playlists/%s/tracks' % shuffler_playlist_id,
                          headers=auth_header,
                          data=json.dumps(track_uris))
            track_uris['uris'].clear()
    if len(track_uris['uris']) is not 0:
        requests.post('https://api.spotify.com/v1/playlists/%s/tracks' % shuffler_playlist_id,
                      headers=auth_header,
                      data=json.dumps(track_uris))
