import datetime
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    name = db.Column(db.String(20)) # name
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):         
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key
    title = db.Column(db.String(60))    # movie title
    year = db.Column(db.String(4))  # movie year
    poster = db.Column(db.String(256))
    review = db.Column(db.Text)
    time = db.Column(db.DateTime)
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    data = db.Column(db.BLOB)