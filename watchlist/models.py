
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    name = db.Column(db.String(40)) # name
    username = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, default=db.func.now())
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

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
    time = db.Column(db.DateTime, default=db.func.now())
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    username = db.Column(db.String(40))
    name = db.Column(db.String(40))


    