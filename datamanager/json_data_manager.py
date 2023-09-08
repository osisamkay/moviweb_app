import json
from datamanager.data_manager_interface import DataManagerInterface


def _generate_unique_id(users):
    if not users:
        return 1
    else:
        max_id = max(user['id'] for user in users)
        return max_id + 1


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """
        Retrieves all the users from the JSON file.

        Returns:
        - list: List of user dictionaries.
        """
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data

    def get_user_movies(self, user_id):
        """
        Retrieves the movies for a specific user from the JSON file.

        Parameters:
        - user_id (int): The ID of the user.

        Returns:
        - list: List of movie dictionaries for the specified user.
        """
        with open(self.filename, 'r') as file:
            data = json.load(file)
            for user in data:
                if user['id'] == user_id:
                    return user['movies']
            return []

    def add_user(self, name, age):
        """
        Adds a new user to the JSON file.

        Parameters:
        - name (str): The name of the user.
        - age (int): The age of the user.

        Returns:
        - int: The ID of the newly added user.
        """
        with open(self.filename, 'r') as file:
            users = json.load(file)

        user_id = _generate_unique_id(users)

        new_user = {
            'id': user_id,
            'name': name,
            'age': age,
            'movies': []
        }

        users.append(new_user)

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

        return user_id

    def get_user(self, user_id):
        """
        Retrieves the user with the specified user ID from the JSON file.

        Parameters:
        - user_id (int): The ID of the user to retrieve.

        Returns:
        - dict or None: The user dictionary if found, or None if the user ID is not found.
        """
        with open(self.filename, 'r') as file:
            users = json.load(file)

            user = next((user for user in users if user['id'] == user_id), None)
            return user

    def add_user_movie(self, user_id, name, director, year, rating):
        """
        Adds a movie to a user's list of movies in the JSON file.

        Parameters:
        - user_id (int): The ID of the user.
        - name (str): The name of the movie.
        - director (str): The director of the movie.
        - year (int): The release year of the movie.
        - rating (float): The rating of the movie.

        Returns:
        - None
        """
        with open(self.filename, 'r') as file:
            users = json.load(file)

        user = next((user for user in users if user_id == user["id"]), None)

        if user is not None:
            movie_id = _generate_unique_id(user["movies"])

            new_movie = {
                "id": movie_id,
                "name": name,
                "director": director,
                "year": year,
                "rating": rating
            }

            user["movies"].append(new_movie)

            with open(self.filename, 'w') as file:
                json.dump(users, file, indent=4)

    def update_user_movie(self, user_id, movie_id, name, director, year, rating):
        """
        Updates the details of a movie in a user's list of movies in the JSON file.

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
        with open(self.filename, 'r') as file:
            users = json.load(file)

        user = next((user for user in users if user['id'] == user_id), None)
        if user is None:
            return False  # User not found

        movie = next((movie for movie in user['movies'] if movie['id'] == movie_id), None)
        if movie is None:
            return False  # Movie not found

        movie['name'] = name
        movie['director'] = director
        movie['year'] = year
        movie['rating'] = rating

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

        return True  # Movie updated successfully

    def delete_user_movie(self, user_id, movie_id):
        """
        Deletes a movie from a user's list of movies in the JSON file.

        Parameters:
        - user_id (int): The ID of the user.
        - movie_id (int): The ID of the movie.

        Returns:
        - bool: True if the movie is deleted successfully, False otherwise.
        """
        with open(self.filename, 'r') as file:
            users = json.load(file)

        user = next((user for user in users if user['id'] == user_id), None)
        if user is None:
            return False  # User not found

        movie = next((movie for movie in user['movies'] if movie['id'] == movie_id), None)
        if movie is None:
            return False  # Movie not found

        user['movies'].remove(movie)

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

        return True  # Movie deleted successfully
