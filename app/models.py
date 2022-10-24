from app import db


class User(db.Model):
    id = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    access_token = db.Column(db.String(512))
    expiration_time = db.Column(db.Integer)
    refresh_token = db.Column(db.String(256))
    shuffler_playlist = db.Column(db.String(64))
    playlists = db.relationship('Playlist', backref='id', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def get_user_playlists(self):
        return Playlist.query.filter_by(user_id=self.id).all()


class Playlist(db.Model):
    playlist_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(191))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), primary_key=True)
    deleted = db.Column(db.Boolean)

    def __repr__(self):
        return '<Playlist {}>'.format(self.name)
