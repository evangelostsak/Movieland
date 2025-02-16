# This script initializes the database by creating all tables.

from app import app, data_manager
from data_manager.data_models import User, Movie, UserMovie

with app.app_context():
    data_manager.db.create_all()  # Creates all tables 
    print("Databases initialized successfully.")