from data_manager.data_manager_interface import DataManagerInterface
from data_manager.data_models import User, Movie, UserMovie, db
from sqlalchemy.exc import SQLAlchemyError
from movie_fetcher import movie_fetcher_omdb


class SQLiteDataManager(DataManagerInterface):
    """SQLite database manager using sqlalchemy, inherits DataManagerInterface"""

    def __init__(self, app):
        """Initialize database with flask"""
        db.init_app(app)  # Initialize SQLAlchemy with Flask app
        self.db = db

    def get_all_users(self):
        """Get all users from the database"""
        try:
            return self.db.session.query(User).all()

        except SQLAlchemyError as h:
            print(f"Error: {h}")
            return []

    def get_user_movies(self, user_id):
        """Get all Movies for a specific user"""

        try:

            user = self.get_user(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} doesn't exist.")

            movies = (
                self.db.session.query(Movie)
                .join(UserMovie, UserMovie.movie_id == Movie.id)
                .filter(UserMovie.user_id == user_id)
                .all()
            )

            if not movies:
                raise ValueError(f"There are no Movies for the given userID {user_id}.")

            return movies
        except ValueError as no_id_err:
            raise ValueError(f"Unable to retrieve movies for userID '{user_id}': {no_id_err}")
        except SQLAlchemyError as h:
            print(f"Error: {h}")
            raise

    def get_user(self, user_id):
        """Get a user by ID"""

        try:
            user = self.db.session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise ValueError(f"No user found with ID {user_id}")
            return user
        except SQLAlchemyError as e:
            print(f"Error fetching user with ID {user_id}: {e}")
            raise

    def add_user(self, user):
        """Add new user to database"""

        try:
            new_user = User(name=user)
            self.db.session.add(new_user)
            self.db.session.commit()
            return f"User {user} has been successfully added!"

        except SQLAlchemyError as e:
            self.db.session.rollback()
            return f"Error adding user '{user}': {e}"

    def delete_user(self, user_id):
        """Deletes user and their entries from the database"""

        # check if user exists
        try:
            del_user = self.get_user(user_id)
            if not del_user:
                return f" User with ID {user_id} does not exist."

            self.db.session.query(UserMovie).filter(UserMovie.user_id == user_id).delete()
            self.db.session.delete(del_user)
            self.db.session.commit()
            return f"User with ID '{user_id}' and their entries are successfully deleted."

        except SQLAlchemyError as e:
            print(f"Error deleting user with ID {user_id}: {e}")
            self.db.session.rollback()

    def update_user(self, user_id, user_name):
        """Update user's name in database"""

        # check if user exists
        try:
            update_user = self.get_user(user_id)
            if not update_user:
                return f" User with ID {user_id} does not exist."
            update_user.name = user_name
            self.db.session.commit()
            return f"User '{user_name}' was updated successfully."

        except SQLAlchemyError as e:
            print(f"Error updating user with ID {user_id}: {e}")
            self.db.session.rollback()

    def get_movie(self, movie_id):
        """Get a movie by its ID"""
        try:
            movie = self.db.session.query(Movie).filter(Movie.id == movie_id).one_or_none()
            if not movie:
                raise ValueError(f"No user found with ID {movie_id}")
            return movie
        except SQLAlchemyError as e:
            print(f"Error fetching user with ID {movie_id}: {e}")
            raise

    def add_movie(self, user_id, title, director=None, release_year=None, rating=None, poster=None):
        """Adds new movie to the database, omdb API used"""

        try:
            # Fetch additional movie data from OMDb if not provided
            movie_data = movie_fetcher_omdb(title)
            if movie_data:
                director = director or movie_data['director']
                rating = rating or movie_data['rating']
                poster = poster or movie_data['poster']
                release_year = release_year or movie_data['release_year']

            # Check if the movie already exists in the database
            existing_movie = (
                self.db.session.query(Movie)
                .filter_by(title=title, release_year=release_year)
                .first()
                )
            if not existing_movie:
                new_movie = Movie(
                    title=title,
                    director=director,
                    release_year=release_year,
                    rating=rating,
                    poster=poster
                )
                self.db.session.add(new_movie)
                self.db.session.commit()
                movie_id = new_movie.id
            else:
                movie_id = existing_movie.id

            user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self.db.session.add(user_movie)
            self.db.session.commit()

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.session.rollback()

    def update_movie(self, movie_id, user_id, rating=None):
        """Update a movie in the database"""
        try:
            update_movie = self.get_movie(movie_id)
            if not update_movie:
                print(f"Movie {movie_id} does not exist.")
            update_movie.rating = rating
            self.db.session.commit()

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.session.rollback()

    def delete_movie(self, movie_id, user_id):
        """
        Deletes the connection between user and movie
        if no other user has this movie, delete the movie from the database
        """
        try:
            user_movie = self.db.session.query(UserMovie).filter_by(user_id=user_id,
                                                                    movie_id=movie_id).first()

            if not user_movie:
                return None  # None if no relationship between user and movie

            movie = self.db.session.query(Movie).filter_by(id=movie_id).first()

            if not movie:
                return None  # None if no movie exists with this ID

            self.db.session.delete(user_movie)

            # If no other users has this movie
            if not self.db.session.query(UserMovie).filter_by(movie_id=movie_id).first():
                self.db.session.delete(movie)

            self.db.session.commit()

            return movie

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.session.rollback()
            return None

    def get_all_movies(self):
        """Gets all the movies in the database"""
        try:
            return self.db.session.query(Movie).all()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            return []
