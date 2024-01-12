"""
Model for using SQLAlchemy ORM.
"""
import datetime
from flask_login import UserMixin
from . import db
# Use below import for sqlalchemy 3.0 approach with Base model
# from sqlalchemy import Column, Integer, String, Float


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text)
    create_ts = db.Column(db.TIMESTAMP)
    fav_mov1 = db.Column(db.Integer, db.ForeignKey('movie.id'))
    fav_mov2 = db.Column(db.Integer, db.ForeignKey('movie.id'))
    fav_mov3 = db.Column(db.Integer, db.ForeignKey('movie.id'))
    fav_genre1 = db.Column(db.String(30))
    fav_genre2 = db.Column(db.String(30))
    fav_genre3 = db.Column(db.String(30))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    avg_rate = db.Column(db.Float)
    imdb_id = db.Column(db.Integer)
    tmdb_id = db.Column(db.String(30))

    genres = db.relationship('MovieGenre', backref='movie')
    tags = db.relationship('MovieTag', backref='movie')


class MovieGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    genre = db.Column(db.String(40))


class MovieRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    rating = db.Column(db.Float)
    create_ts = db.Column(db.TIMESTAMP)


class MovieTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    tag = db.Column(db.String(100))
    create_ts = db.Column(db.Integer)

