from data_manager.data_manager_interface import DataManagerInterface
from data_manager.data_models import User, Movie, UserMovie


class SQLiteDataManager(DataManagerInterface):

    def __init__(self):
        pass

    def get_all_users(self):
        pass

    def get_user_movies(self, user_id):
        pass

    def add_user(self, user):
        pass

    def delete_user(self, user_id):
        pass

    def update_user(self, user_id):
        pass

    def add_movie(self, title, director, year, rating):
        pass

    def update_movie(self, movie_id, title, director, year, rating):
        pass

    def delete_movie(self, movie_id):
        pass

    def get_all_movies(self):
        pass
