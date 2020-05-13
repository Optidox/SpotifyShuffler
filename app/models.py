from app import db
from flask import session


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    refresh_token = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)
