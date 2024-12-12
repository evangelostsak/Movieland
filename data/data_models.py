from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):
    pass


class Movie(db.Model):
    pass


class UserMovie(db.Model):
    pass
