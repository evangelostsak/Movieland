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
data = SQLiteDataManager(app)

# Table creation, run only once
# with app.app_context():
#     data.db.create_all()


