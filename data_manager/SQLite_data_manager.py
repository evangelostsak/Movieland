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

    def register(self, username, password):
        """Registers new user to database"""

        try:
            existing_user = self.db.session.query(User).filter_by(username=username).first()
            if existing_user:
                return f"User {username} already exists!"
            new_user = User(username=username)
            new_user.set_password(password)
            self.db.session.add(new_user)
            self.db.session.commit()

            return f"User {username} has been successfully created!"
        except Exception as e:
            self.db.session.rollback()
            return f"Error: {str(e)}"

    def delete_user(self, user_id):
        """Deletes user and their entries from the database"""

        # check if user exists
        try:
            del_user = self.get_user(user_id)
            if not del_user:
                return f" User with ID {user_id} does not exist."

            # Get all movies associated with the user
            user_movies = self.db.session.query(UserMovie).filter_by(user_id=user_id).all()
            movie_ids = [user_movie.movie_id for user_movie in user_movies]

            # delete all UserMovie relationships for this user
            self.db.session.query(UserMovie).filter_by(user_id=user_id).delete()

            # check if any of the movies are not associated with other users
            for movie_id in movie_ids:
                is_movie_linked = self.db.session.query(UserMovie).filter_by(movie_id=movie_id).first()
                if not is_movie_linked:
                    # if movie is not linked to any other user
                    movie = self.db.session.query(Movie).get(movie_id)
                    if movie:
                        # delete the movie
                        self.db.session.delete(movie)
            self.db.session.delete(del_user)
            self.db.session.commit()
            return f"User with ID '{user_id}' and their entries are successfully deleted."

        except SQLAlchemyError as e:
            self.db.session.rollback()
            return f"Error deleting user with ID {user_id}: {e}"

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
            self.db.session.rollback()
            return f"Error updating user with ID {user_id}: {e}"

    def get_movie(self, movie_id):
        """Get a movie by its ID"""
        try:
            movie = self.db.session.query(Movie).filter(Movie.id == movie_id).one_or_none()
            if not movie:
                raise ValueError(f"No movie found with ID {movie_id}")
            return movie
        except SQLAlchemyError as e:
            print(f"Error fetching movie with ID {movie_id}: {e}")
            raise

    def add_movie(self, user_id, title, director=None,
                  release_year=None, rating=None, poster=None, link=None, likes=0):
        """Adds a new movie to the database."""
        try:
            # Fetch movie data from OMDb
            movie_data = movie_fetcher_omdb(title)

            if not movie_data:  # Movie not found in OMDb
                print(f"No movie found with the title '{title}'.")
                return None

            # Check if the movie already exists
            existing_movie = (
                self.db.session.query(Movie)
                .filter_by(title=title, release_year=movie_data['release_year'])
                .first()
            )
            if existing_movie:
                movie_id = existing_movie.id
            else:
                # Create a new movie entry
                new_movie = Movie(
                    title=title,
                    director=movie_data['director'],
                    release_year=movie_data['release_year'],
                    rating=movie_data['rating'],
                    poster=movie_data['poster'],
                    link=f"https://www.imdb.com/title/{movie_data['link']}",
                    likes=likes

                )
                self.db.session.add(new_movie)
                self.db.session.commit()
                movie_id = new_movie.id

            # Add relationship with the user
            user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self.db.session.add(user_movie)
            self.db.session.commit()

            return True  # Success

        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            self.db.session.rollback()
            return None  # Failure

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

    def like_movie(self, movie_id):
        """Increments the likes for a specific movie."""
        try:
            movie = self.db.session.query(Movie).filter_by(id=movie_id).first()
            if not movie:
                return None  # Movie not found

            movie.likes += 1
            self.db.session.commit()

            return movie  # Return the updated movie object

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.session.rollback()
            return None
        
    def get_user_by_username(self, username):
        """Get a user by their username"""

        try:
            user = self.db.session.query(User).filter_by(username=username).first()
            return user
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            return None
        
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""

        try:
            user = self.get_user_by_username(username)
            if user and User.check_password_hash(user.password, password):
                return user
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            return None
