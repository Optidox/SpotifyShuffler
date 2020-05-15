from app import db
from flask import session


class User(db.Model):
    id = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    access_token = db.Column(db.String(64))
    expiration_time = db.Column(db.Integer)
    refresh_token = db.Column(db.String(64))
    shuffled_playlist = db.Column(db.String(64))
    playlists = db.relationship('Playlist', backref='id', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def get_user_playlists(self):
        return Playlist.query.get(user_id=self.id).all()

class Playlist(db.Model):
    playlist_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), primary_key=True)
    deleted = db.Column(db.Bool)

    def __repr__(self):
        return '<Playlist {}>'.format(self.name)
