from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):
    """
    Model for Users
    """
    __table_name__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Relationship update
    user_movies = relationship('UserMovie', backref='user', cascade='all, delete', lazy=True)


class Movie(db.Model):
    """
    Model for Movies
    """
    __table_name__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    director = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    poster = Column(String, nullable=True)

    # Relationship update
    user_movies = relationship('UserMovie', backref='movie', cascade='all, delete', lazy=True)


class UserMovie(db.Model):
    """
    Model for relationship between users and movies
    """
    __table_name__ = 'user_movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
