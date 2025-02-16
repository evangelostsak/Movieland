from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin,db.Model):
    """
    Model for Users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String,unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password."""
        return check_password_hash(self.password_hash, password)


    # Relationship with UserMovie
    user_movies = relationship('UserMovie', back_populates='user', cascade='all, delete')

    def __str__(self):
        """ Human-readable presentation of the model user"""
        return f"{self.id}. {self.username}"

    def __repr__(self):
        """Returns a string representation of the User model, debugging-friendly"""
        return f"User(id = {self.id}, name = {self.username})"


class Movie(db.Model):
    """
    Model for Movies
    """
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    director = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    poster = Column(String, nullable=True)
    link = Column(String, nullable=True)
    likes = Column(Integer, default=0)

    # Relationship with UserMovie
    user_movies = relationship('UserMovie', back_populates='movie', cascade='all, delete')

    def __str__(self):
        """Human-readable string representation of the model Movie"""
        return f"{self.id}. {self.title}, {self.release_year}"

    def __repr__(self):
        """Returns a string representation of the Movie model, debugging-friendly"""
        return (f"Movie(id = {self.id}, title = {self.title}, release_year = {self.release_year}, "
                f"poster = {self.poster}, director = {self.director}, rating = {self.rating}, "
                f"link = {self.link}), likes = {self.likes}")


class UserMovie(db.Model):
    """
    Model for relationship between users and movies
    """
    __tablename__ = 'user_movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='user_movies')
    movie = relationship('Movie', back_populates='user_movies')

    def __repr__(self):
        """Returns a string representation of the UserMovie model, debugging-friendly"""
        return f"UserMovie(id = {self.id}, user_id = {self.user_id}, movie_id = {self.movie_id})"
