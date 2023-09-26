from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users.

        Returns:
        - list: List of user dictionaries.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves the movies for a specific user.

        Parameters:
        - user_id (int): The ID of the user.

        Returns:
        - list: List of movie dictionaries for the specified user.
        """
        pass

    @abstractmethod
    def add_user(self, name, age):
        """
        Adds a new user.

        Parameters:
        - name (str): The name of the user.
        - age (int): The age of the user.

        Returns:
        - int: The ID of the newly added user.
        """
        pass

    @abstractmethod
    def get_user(self, user_id):
        """
        Retrieves the user with the specified user ID.

        Parameters:
        - user_id (int): The ID of the user to retrieve.

        Returns:
        - dict or None: The user dictionary if found, or None if the user ID is not found.
        """
        pass

    @abstractmethod
    def add_user_movie(self, user_id, name, director, year, rating):
        """
        Adds a movie to a user's list of movies.

        Parameters:
        - user_id (int): The ID of the user.
        - name (str): The name of the movie.
        - director (str): The director of the movie.
        - year (int): The release year of the movie.
        - rating (float): The rating of the movie.

        Returns:
        - None
        """
        pass

    @abstractmethod
    def update_user_movie(self, user_id, movie_id, name, director, year, rating):
        """
        Updates the details of a movie in a user's list of movies.

        Parameters:
        - user_id (int): The ID of the user.
        - movie_id (int): The ID of the movie.
        - name (str): The updated name of the movie.
        - director (str): The updated director of the movie.
        - year (int): The updated release year of the movie.
        - rating (float): The updated rating of the movie.

        Returns:
        - bool: True if the movie is updated successfully, False otherwise.
        """
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        """
        Deletes a movie from a user's list of movies.

        Parameters:
        - user_id (int): The ID of the user.
        - movie_id (int): The ID of the movie.

        Returns:
        - bool: True if the movie is deleted successfully, False otherwise.
        """
        pass
