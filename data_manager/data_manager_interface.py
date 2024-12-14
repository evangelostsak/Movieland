from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Defines abstract class for DataManagerInterface
    Will be used to create the DataManager class.
    """

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def update_user(self, user_id, user_name):
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        pass

    @abstractmethod
    def add_movie(self, user_id, title, director, release_year, rating, poster):
        pass

    @abstractmethod
    def update_movie(self, movie_id, rating):
        pass

    @abstractmethod
    def delete_movie(self, movie_id, user_id):
        pass

    def get_all_movies(self):
        pass
