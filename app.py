import os
import sqlalchemy
import logging
from flask import Flask, request, render_template, redirect, flash, url_for, session
from data_manager.SQLite_data_manager import SQLiteDataManager
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure SQLite URI
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/movies.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure file upload settings
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize DataManager
data_manager = SQLiteDataManager(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "error"


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
            flash(f"{message}", "error")
            logger.warning(f"Registration failed: {message}")
            return render_template("register.html")
        
        flash(f"{message}", "success")
        logger.info(f"New user registered: {username}")
        return redirect(url_for('login'))
    
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        flash("Error while adding the user, please try again!", "error")
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
            flash(f"Welcome back, {user.username}!", "success")
            logger.info(f"User logged in: {user.username}")
            return redirect(url_for('home'))
        
        else:
            flash("Invalid username or password. Please try again.", "error")
            logger.warning("Failed login attempt.")

    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """Logout route"""

    user = data_manager.get_user(current_user.id)
    if request.method == "POST":
        logout_user()
        flash("You have been logged out.", "success")
        logger.info(f"User logged out: {user.username}")
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
def user_profile(user_id):
    """Displaying list of movies of a user"""

    if int(current_user.id) != int(user_id):
        flash("You can only see your own Movies.", "error")
        return redirect(url_for("home"))

    user_name = data_manager.get_user(user_id)
    if not user_name:
        raise NotFound

    try:
        message = request.args.get('message')
        if message:
            flash(message)
    except Exception as e:
        logger.error(f"Error fetching user movies: {e}")
        flash("Couldn't find any Movies. Try adding some.", "info")
        movies = []

    return render_template('profile.html', user=user_name)


@app.route("/users/<user_id>/movies", methods=["GET"])
@login_required
def user_movies(user_id):
    """Displaying list of movies of a user"""

    if int(current_user.id) != int(user_id):
        flash("You can only see your own Movies.", "error")
        return redirect(url_for("home"))

    user_name = data_manager.get_user(user_id)
    if not user_name:
        raise NotFound

    try:
        movies = data_manager.get_user_movies(user_id)
        message = request.args.get('message')
        if message:
            flash(message)
    except Exception as e:
        logger.error(f"Error fetching user movies: {e}")
        flash("Couldn't find any Movies. Try adding some.", "info")
        movies = []

    return render_template('user_movies.html', user=user_name, movies=movies)


@app.route("/users/<user_id>/update_user", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    """Update a users details"""

    if int(current_user.id) != int(user_id):
        flash("You can only update your own profile.", "error")
        return redirect(url_for("home"))
    
    user = data_manager.get_user(user_id)
    if not user:
        raise NotFound
    
    if request.method == "GET":
        return render_template("update_user.html", user=user, user_id=user_id)

    if request.method == "POST":

        user_name = request.form.get("name").strip()
        password = request.form.get("password").strip()
        file = request.files.get("profile_picture")
        remove_profile_picture = request.form.get("remove_profile_picture")
        filename = None
        
        try:
            if remove_profile_picture:
                 filename = "default.png"

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

            # Update all user details
            message = data_manager.update_user(
                user_id=user_id,
                user_name=user_name if user_name else user.username,
                password=password if password else user.password_hash,
                profile_picture=filename if (file or remove_profile_picture) else user.profile_picture)
                
        except Exception as e:
            flash(f"Error updating user, try that again!", "error")
            logger.error(f"Error updating user: {e}")
            return redirect(f"/users/{user_id}/update_user")

        flash(f"{message}", "success")
        logger.info(f"User details updated: {user.username}")
        return redirect(f"/users/{user_id}")


@app.route("/users/<user_id>/delete_user", methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    """Delete target user from the database"""

    if int(current_user.id) != int(user_id):
        flash("You can only delete your own profile.", "error")
        return redirect(url_for("home"))
    
    user = data_manager.get_user(user_id)
    if not user:
        raise NotFound
    
    if request.method == "GET":
        return render_template("delete_user.html", user=user, user_id=user_id)
    
    if request.method == "POST":

        try:
            user_id = current_user.id
            del_user = data_manager.delete_user(user_id)
            if not del_user:
                flash(f"User with ID {user_id} couldn't be found.", "error")
                return redirect('home')
            flash(f"User '{user_id}' has been deleted successfully!", "success")
            logout_user()
            logger.info(f"User '{user.username}' has been deleted.")
            return redirect(url_for("login"))

        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            flash("An error occurred while deleting the user. Please try again.", "error")
            return redirect(url_for("home"))


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
@login_required
def add_movie(user_id):
    """Logged in user can add movies to their account."""

    if int(current_user.id) != int(user_id):
        flash("You can only add movies to your own profile.", "error")
        return redirect(url_for("home"))
    
    # Fetch user details for display or validation
    user = data_manager.get_user(user_id)

    if not user:
        raise NotFound

    if request.method == "GET":
        return render_template("add_movie.html", user=user)

    if request.method == "POST":
        title = request.form.get('title', '').strip()

        # Validate input
        if not title:
            flash("Title is required.", "error")
            return render_template("add_movie.html", user=user)

        try:
            result = data_manager.add_movie(user_id, title)

            # Check the result of add_movie
            if result is None:  # Movie not found or failed to add
                flash(f"Movie '{title}' doesn't exist. Make sure the title is correct.", "error")
                return render_template("add_movie.html", user=user)

        except Exception as e:
            logger.error(f"Error adding movie: {e}")
            flash("An error occurred while adding the movie. Please try again.", "error")
            return render_template("add_movie.html", user=user)

        flash(f"Movie '{title}' has been added successfully.", "success")
        logger.info(f"Movie '{title}' has been added by {user.username}")
        return redirect(f"/users/{user_id}/movies")


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
@login_required
def update_movie(user_id, movie_id):
    """Updates a movie of a specific user"""

    if int(current_user.id) != int(user_id):
        flash("You can only add movies to your own profile.", "error")
        return redirect(url_for("home"))
    
    user = data_manager.get_user(user_id)

    if request.method == "GET":

        movie = data_manager.get_movie(movie_id)
        if not movie:
            return NotFound
        return render_template('update_movie.html', movie=movie, user_id=user_id)

    if request.method == "POST":
        personal_rating = request.form.get('rating').strip()
        movie = data_manager.get_movie(movie_id)

        try:
            data_manager.update_movie(movie_id=movie_id, user_id=user_id, rating=personal_rating)
        except Exception as e:
            logger.error(f"Error updating movie: {e}")
            flash("Error while updating movie. Try again!", "error")
            return render_template('update_movie.html', movie=data_manager.get_movie(movie_id),
                                   user_id=user_id)

        flash(f"Movie '{movie.title}' has been updated successfully!", "success")
        logger.info(f"Movie '{movie.title}' has been updated by {user.username}")
        return redirect(f"/users/{user_id}/movies")


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET"])
@login_required
def delete_movie(user_id, movie_id):
    """Deletes a user's movie"""

    user = data_manager.get_user(user_id)   
    try:
        del_movie = data_manager.delete_movie(movie_id, user_id)

        if not del_movie:
            flash(f"Movie '{movie_id}' not found.")
            return redirect(f"/users/{user_id}/movies")

        flash(f"Movie '{del_movie.title}' has been deleted successfully!", "success")
        logger.info(f"Movie '{del_movie.title}' has been deleted by {user.username}")
        return redirect(f"/users/{user_id}/movies")

    except Exception as e:
        logger.error(f"Error deleting movie: {e}")
        flash(f"""An error occurred while deleting the movie. Please try again.""", "error")
        return redirect(f"/users/{user_id}/movies")


@app.route('/movies/likes/<int:movie_id>', methods=["POST"])
@login_required
def like_movie(movie_id):
    """Adds liking for a specific movie in general movie list"""
    try:
        movie = data_manager.like_movie(movie_id)
        if not movie:
            flash("Movie not found!", "error")
            return redirect(url_for('list_movies'))

        flash(f"Movie '{movie.title}' has been liked!", "success")
        logger.info(f"Movie '{movie.title}' has been liked by {current_user.username}")
        return redirect(url_for('list_movies', movie_id=movie.id))  # Redirect to the movie details page

    except Exception as e:
        logger.error(f"Error liking movie: {e}")
        flash("An error occurred while liking the movie.", "error")
        return redirect(url_for('list_movies'))


@app.errorhandler(404)
def page_not_found(e):
    """404 Error handling route"""

    logger.warning(f"404 Error: {request.url} not found")
    return render_template('404.html'), 404


@app.errorhandler(500)
def network_error(e):
    """500 error handling route"""

    logger.error(f"500 Internal Server Error: {str(e)}")
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
