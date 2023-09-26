from flask_sqlalchemy import SQLAlchemy

from datamanager.data_manager_interface import DataManagerInterface
from model import User, Movie, Favorites, Review
import requests

db = SQLAlchemy()


class MovieNotFoundException(Exception):
    pass


def search_movie(title):
    """
    Search for a movie using the Omdb API.

    Args:
        title (str): The title of the movie to search.

    Returns:
        dict: Movie details obtained from the Omdb API.

    Raises:
        MovieNotFoundException: If the movie is not found.
    """
    url = f"http://www.omdbapi.com/?t={title}&apikey=608f304e"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        data = response.json()

        # Check if the API response indicates that the movie was not found
        if 'Error' in data and data['Error'] == 'Movie not found!':
            raise MovieNotFoundException(f"Movie not found: {title}")

        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # Handle network errors or API request failures here
        raise  # Re-raise the exception for higher-level handling
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception for higher-level handling


class SQLiteDataManager(DataManagerInterface):
    """
    Implementation of DataManagerInterface using SQLite and SQLAlchemy.
    """

    def __init__(self, app):
        """
        Initialize the SQLiteDataManager.

        Args:
            app (Flask): The Flask application instance.
        """
        db.init_app(app)  # Initialize db with the Flask app
        self.db = db

    def get_all_users(self):
        """
        Get a list of all users.

        Returns:
            list: List of serialized user dictionaries with 'id', 'username', and 'age'.
        """
        users = db.session.query(User).all()
        serialized_users = [{'id': user.id, 'username': user.username, 'age': user.age} for user in users]
        return serialized_users

    def get_user_movies(self, user_id):
        """
        Get a list of movies favorited by a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: List of Movie objects favorited by the user.
        """
        movies = (
            self.db.session.query(Movie)
            .join(Favorites, Movie.id == Favorites.movie_id)
            .filter(Favorites.user_id == user_id)
            .all()
        )
        return movies

    def add_user(self, name, age):
        """
        Add a new user to the database.

        Args:
            name (str): The username of the user.
            age (int): The age of the user.

        Returns:
            int: The ID of the newly added user.
        """
        new_user = User(username=name, age=age)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id

    def get_movie(self, movie_id):
        """
        Get details of a movie by its ID.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            dict: A dictionary containing movie details with 'id', 'name', 'director', 'year', and 'rating'.
                Returns None if the movie is not found.
        """
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return {
                'id': movie.id,
                'name': movie.title,
                'director': movie.director,
                'year': movie.year,
                'rating': movie.rating
            }
        return None

    def get_user(self, user_id):
        """
        Get details of a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: A dictionary containing user details with 'id', 'username', and 'age'.
                Returns None if the user is not found.
        """
        user = db.session.query(User).get(user_id)
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'age': user.age
            }
        return None

    def add_user_movie(self, user_id, title, director, year, rating):
        """
        Add a new movie to a user's list of favorite movies.

        Args:
            user_id (int): The ID of the user.
            title (str): The title of the movie.
            director (str): The director of the movie.
            year (str): The release year of the movie.
            rating (int): The rating of the movie.
        """
        user = db.session.query(User).get(user_id)
        if user:
            new_movie = Movie(title=title, director=director, year=year, rating=rating)
            user.favorite_movies.append(new_movie)
            db.session.commit()

    def update_user_movie(self, user_id, movie_id, name, director, year, rating):
        """
        Update the details of a movie in a user's list of favorite movies.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            name (str): The updated title of the movie.
            director (str): The updated director of the movie.
            year (str): The updated release year of the movie.
            rating (int): The updated rating of the movie.

        Returns:
            bool: True if the update was successful, False if the movie or user is not found.
        """
        movie = db.session.query(Movie).get(movie_id)
        if movie and movie in db.session.query(User).get(user_id).favorite_movies:
            movie.title = name
            movie.director = director
            movie.year = year
            movie.rating = rating
            db.session.commit()
            return True
        return False

    def delete_user_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's list of favorite movies.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            bool: True if the deletion was successful, False if the movie or user is not found.
        """
        user = db.session.query(User).get(user_id)
        movie = db.session.query(Movie).get(movie_id)
        if user and movie and movie in user.favorite_movies:
            user.favorite_movies.remove(movie)
            db.session.commit()
            return True
        return False

    def add_review(self, user_id, movie_id, review_text, rating):
        """
        Add a review for a movie by a user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            review_text (str): The review text.
            rating (float): The rating of the movie.

        Returns:
            None
        """
        review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
        db.session.add(review)
        db.session.commit()

    def get_movie_reviews(self, movie_id):
        """
        Get a list of reviews for a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            list: List of Review objects for the movie.
        """
        reviews = db.session.query(Review).filter_by(movie_id=movie_id).all()
        return reviews
