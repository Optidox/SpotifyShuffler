from app import db
from flask import session


class User(db.Model):
    id = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    access_token = db.Column(db.String(64))
    expiration_time = db.Column(db.Integer)
    refresh_token = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def load_user(id):
        return User.query.get(str(id))
