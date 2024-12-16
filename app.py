import os
import sqlalchemy
from flask import Flask, request, render_template, redirect, flash
from data_manager.SQLite_data_manager import SQLiteDataManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure SQLite URI
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/movies.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DataManager
data_manager = SQLiteDataManager(app)

# Table creation, run only once
# with app.app_context():
#     data.db.create_all()


@app.route("/", methods=["GET"])
def home():
    """Flask route for homepage, home.html gets rendered"""
    return render_template("home.html")


@app.route("/users", methods=["GET"])
def list_users():
    """Display all users in the database"""
    users = data_manager.get_all_users()
    message = request.args.get('message')
    if message:
        flash(message)
    return render_template("users.html", users=users)


@app.route("/movies", methods=["GET"])
def list_movies():
    """Display all movies in the database"""
    movies = data_manager.get_all_movies()
    message = request.args.get('message')
    if message:
        flash(message)
    return render_template("movies.html", movies=movies, message=message)


@app.route("/users/<user_id>", methods=["GET"])
def user_movies(user_id):
    """Displaying list of movies of a user"""
    try:
        user_name = data_manager.get_user(user_id)
        if not user_name:
            return redirect('/404')
    except sqlalchemy.exc.NoResultFound:
        return redirect('/404')

    try:
        movies = data_manager.get_user_movies(user_id)
        message = request.args.get('message')
        if message:
            flash(message)
    except Exception as e:
        print(f"Error fetching movies for user {user_id}: {e}")
        movies = []

    return render_template('user_movies.html', user=user_name, movies=movies)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """Add a user in the database"""

    if request.method == "GET":
        return render_template("add_user.html")

    if request.method == "POST":
        name = request.form.get('name').strip()

        if not name:
            flash("Name is mandatory!")
            return render_template("add_user.html")
        if len(name) < 3:
            flash("Name must contain at-least 3 characters.")
            return render_template("add_user.html")
        if len(name) > 20:
            flash("Name cannot have more than 20 characters.")
            return render_template("add_user.html")

        try:
            data_manager.add_user(name)
        except Exception as e:
            flash("Error while adding the user, please try again!")
            flash(f"Error: {e}")
            return render_template("add_user.html")

        flash(f"User {name} has been added successfully!")
        return render_template("add_user.html")


@app.route("/users/<user_id>/update_user", methods=["GET", "POST"])
def update_user(user_id):
    """Update a users details"""
    if request.method == "GET":
        try:
            user = data_manager.get_user(user_id)
        except sqlalchemy.exc.NoResultFound:
            return redirect('/404')
        return render_template("update_user.html", user=user, user_id=user_id)

    if request.method == "POST":
        user_name = request.form.get("name").strip()
        if not user_name:
            flash("Username can't be empty.")
            try:
                user = data_manager.get_user(user_id)
            except sqlalchemy.exc.NoResultFound:
                return redirect('/404')
            return render_template('update_user.html', user=user, user_id=user_id)
        try:
            # Update user details
            data_manager.update_user(user_id=user_id, user_name=user_name)
            user = data_manager.get_user(user_id)
        except Exception as e:
            flash(f"Error updating user: {e}")
            try:
                user = data_manager.get_user(user_id)
            except sqlalchemy.exc.NoResultFound:
                return redirect('/404')
            return render_template('update_user.html', user=user, user_id=user_id)

        flash(f"User {user_name} has been updated successfully!")
        return render_template("update_user.html", user=user, user_id=user_id)


@app.route("/users/<user_id>/delete_user", methods=["GET"])
def delete_user(user_id):
    """Delete target user from the database"""
    try:
        del_user = data_manager.delete_user(user_id)
        if not del_user:
            message = f"User with ID {user_id} couldn't be found."
            return redirect(f'/users?=message={message}')
        # message = f"User {del_user} has been deleted successfully!"
        return redirect(f'/users?message={del_user}')

    except Exception as e:
        print(f"Error deleting user: {e}")
        message = "An error occurred while deleting the user. Please try again."
        return redirect(f'/users?message={message}')


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """Add movie to a specific room"""
    try:
        user_name = data_manager.get_user(user_id)
    except sqlalchemy.exc.NoResultFound:
        return redirect('/404')

    if request.method == "GET":
        return render_template("add_movie.html", user=user_name)

    if request.method == "POST":
        title = request.form.get('title', '').strip()
        if not title:
            flash("Title is required.")
            return render_template("add_movie.html")

        try:
            data_manager.add_movie(user_id, title)

        except Exception as e:
            print(f"Error: {e}")
            flash("Error while adding movie. Try again!")
            return render_template('add_movie.html', user=user_name)

        flash(f"Movie '{title}' has been added successfully")
        return render_template('add_movie.html', user=user_name)


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """Updates a movie of a specific user"""
    if request.method == "GET":
        try:
            movie = data_manager.get_movie(movie_id)
        except sqlalchemy.exc.NoResultFound:
            return redirect('/404')
        return render_template('update_movie.html', movie=movie, user_id=user_id)

    if request.method == "POST":
        personal_rating = request.form.get('rating').strip()
        movie = data_manager.get_movie(movie_id)

        try:
            data_manager.update_movie(movie_id=movie_id, user_id=user_id, rating=personal_rating)
        except Exception as e:
            print(f"Error: {e}")
            flash("Error while updating movie. Try again!")
            return render_template('update_movie.html', movie=data_manager.get_movie(movie_id),
                                   user_id=user_id)

        flash(f"Movie '{movie.title}' has been updated successfully!")
        return render_template('update_movie.html', movie=data_manager.get_movie(movie_id),
                               user_id=user_id)


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET"])
def delete_movie(user_id, movie_id):
    """Deletes a user's movie"""
    try:
        del_movie = data_manager.delete_movie(movie_id, user_id)

        if not del_movie:
            message = f"Movie '{movie_id}' not found."
            return redirect(f"/users/{user_id}?message={message}")

        message = f"Movie '{del_movie.title}' has been deleted successfully!"
        return redirect(f"/users/{user_id}?message={message}")

    except Exception as e:
        print(f"Error: {e}")
        message = f"Error: {e}"
        return redirect(f"/users/{user_id}?message={message}")


@app.errorhandler(404)
def page_not_found(e):
    """404 Error handling route"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def network_error(e):
    """500 error handling route"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
