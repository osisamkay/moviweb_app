import os

from flask import Blueprint, jsonify, request, Flask
from datamanager.SQLiteDataManager import SQLiteDataManager

app = Flask(__name__, template_folder="templates")

# Create a Blueprint for the API
api = Blueprint('api', __name__)

# Set up the database path
database_path = os.path.abspath('data/moviedb.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

# Initialize the SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)


@api.route('/users', methods=['GET'])
def get_users():
    """
    Get a list of all users.

    Returns:
        JSON response containing the list of users.
    """
    users = data_manager.get_all_users()
    return jsonify(users)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    Get the list of favorite movies for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON response containing the list of favorite movies for the user.
    """
    user = data_manager.get_user(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    movies = data_manager.get_user_movies(user_id)

    serialized_movies = []
    for movie in movies:
        serialized_movie = {
            'id': movie.id,
            'title': movie.title,
            'director': movie.director,
            'year': movie.year,
            'rating': movie.rating
        }
        serialized_movies.append(serialized_movie)

    return jsonify({'movies': serialized_movies})


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    """
    Add a new favorite movie for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON response indicating the status of the movie addition.
    """
    user = data_manager.get_user(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data or 'title' not in data or 'director' not in data or 'year' not in data or 'rating' not in data:
        return jsonify({'error': 'Missing required data'}), 400

    movie = {
        'title': data['title'],
        'director': data['director'],
        'year': data['year'],
        'rating': data['rating']
    }
    data_manager.add_user_movie(user_id, movie['title'], movie['director'], movie['year'], movie['rating'])

    return jsonify({'message': 'Movie added successfully'}), 201
