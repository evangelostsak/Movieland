import os
import sqlalchemy
from flask import Flask, request, render_template, redirect, flash, url_for
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
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@app.route("/movies", methods=["GET"])
def list_movies():
    pass


@app.route("/users/<user_id>", methods=["GET"])
def user_movies(user_id):
    pass


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    pass


@app.route("/update_user", methods=["GET", "POST"])
def update_user(user_id):
    pass


@app.route("/users/<user_id>/delete_user", methods=["GET"])
def delete_user(user_id):
    pass


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    pass


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    pass


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET"])
def delete_movie(user_id, movie_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)


