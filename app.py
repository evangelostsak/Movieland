import os
import sqlalchemy
from flask import Flask, request, render_template, redirect, flash, url_for, session
from data_manager.SQLite_data_manager import SQLiteDataManager
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure SQLite URI
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/movies.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DataManager
data_manager = SQLiteDataManager(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = data_manager.get_user(user_id)
    return user


@app.route("/register", methods=["GET", "POST"])
def register():
    """Add a user in the database"""

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

    if not username:
        flash("Name is mandatory!")
        return render_template("register.html")
    if len(username) < 3:
        flash("Name must contain at-least 3 characters.")
        return render_template("register.html")
    if len(username) > 20:
        flash("Name cannot have more than 20 characters.")
        return render_template("register.html")
    if not password:
        flash("Password is mandatory!")
        return render_template("register.html")
    if len(password) < 6:
        flash("Password must contain at-least 6 characters.")
        return render_template("register.html")
    if len(password) > 20:
        flash("Password cannot have more than 20 characters.")
        return render_template("register.html")

    try:
        message = data_manager.register(username, password)
        if "already exists" in message:
            flash(f"{message}")
            return render_template("register.html")
        
        flash(f"Account for {username} created successfully!")
        return redirect(url_for('login'))
    
    except Exception as e:
        flash("Error while adding the user, please try again!")
        flash(f"Error: {e}")
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route"""

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = data_manager.authenticate_user(username=username, password=password)

        if user: # Only authenticated user can login
            login_user(user)
            flash(f"Welcome back, {user.username}!")
            return redirect(url_for('home'))
        
        else:
            flash("Invalid username or password. Please try again.")

    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """Logout route"""
    if request.method == "POST":
        logout_user()
        flash("You have been logged out.")
        return redirect(url_for('login'))

    return render_template("logout.html")


@app.route("/", methods=["GET"])
def home():
    """Flask route for homepage, home.html gets rendered"""
    return render_template("home.html")


@app.route("/users", methods=["GET"])
def list_users():
    """Display all users in the database"""
    users = data_manager.get_all_users()
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
@login_required
def user_movies(user_id):
    """Displaying list of movies of a user"""

    if int(current_user.id) != int(user_id):
        flash("You can only see your own Movies.")
        return redirect(url_for("home"))
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

    return render_template('profile.html', user=user_name, movies=movies)


@app.route("/users/<user_id>/update_user", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    """Update a users details"""

    if int(current_user.id) != int(user_id):
        flash("You can only update your own profile.")
        return redirect(url_for("home"))
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
@login_required
def delete_user(user_id):
    """Delete target user from the database"""

    if int(current_user.id) != int(user_id):
        flash("You can only delete your own profile.")
        return redirect(url_for("home"))
    try:
        user_id = current_user.id
        del_user = data_manager.delete_user(user_id)
        if not del_user:
            flash(f"User with ID {user_id} couldn't be found.")
            return redirect('home')
        flash(f"User '{user_id}' has been deleted successfully!")
        logout_user()
        return redirect(url_for("login"))

    except Exception as e:
        print(f"Error deleting user: {e}")
        flash("An error occurred while deleting the user. Please try again.")
        return redirect(url_for("home"))


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
@login_required
def add_movie(user_id):
    """Logged in user can add movies to their account."""

    if int(current_user.id) != int(user_id):
        flash("You can only add movies to your own profile.")
        return redirect(url_for("home"))
    
    try:
        # Fetch user details for display or validation
        user_name = data_manager.get_user(user_id)
    except sqlalchemy.exc.NoResultFound:
        return redirect('/404')

    if request.method == "GET":
        return render_template("add_movie.html", user=user_name)

    if request.method == "POST":
        title = request.form.get('title', '').strip()

        # Validate input
        if not title:
            flash("Title is required.")
            return render_template("add_movie.html", user=user_name)

        try:
            result = data_manager.add_movie(user_id, title)

            # Check the result of add_movie
            if result is None:  # Movie not found or failed to add
                flash(f"Movie '{title}' doesn't exist. Make sure the title is correct.")
                return render_template("add_movie.html", user=user_name)

        except Exception as e:
            # Log and display any unexpected errors
            print(f"Error: {e}")
            flash("An error occurred while adding the movie. Please try again.")
            return render_template("add_movie.html", user=user_name)

        # Success case: movie added
        flash(f"Movie '{title}' has been added successfully.")
        return render_template("add_movie.html", user=user_name)


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
@login_required
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
@login_required
def delete_movie(user_id, movie_id):
    """Deletes a user's movie"""
    try:
        del_movie = data_manager.delete_movie(movie_id, user_id)

        if not del_movie:
            flash(f"Movie '{movie_id}' not found.")
            return redirect(f"/users/{user_id}")

        flash(f"Movie '{del_movie.title}' has been deleted successfully!")
        return redirect(f"/users/{user_id}")

    except Exception as e:
        print(f"Error: {e}")
        flash(f"Error: {e}")
        return redirect(f"/users/{user_id}")


@app.route('/movies/likes/<int:movie_id>', methods=["POST"])
@login_required
def like_movie(movie_id):
    """Adds liking for a specific movie in general movie list"""
    try:
        movie = data_manager.like_movie(movie_id)
        if not movie:
            flash("Movie not found!")
            return redirect(url_for('list_movies'))

        flash(f"Movie '{movie.title}' has been liked!")
        return redirect(url_for('list_movies', movie_id=movie.id))  # Redirect to the movie details page

    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while liking the movie.")
        return redirect(url_for('list_movies'))


@app.errorhandler(404)
def page_not_found():
    """404 Error handling route"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def network_error():
    """500 error handling route"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
