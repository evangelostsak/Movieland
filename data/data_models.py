from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    pass


class Movie(db.Model):
    pass


class UserMovie(db.Model):
    pass
