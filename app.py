import os

from flask import Flask, render_template, request, redirect, url_for, flash

from api import api
from datamanager.SQLiteDataManager import SQLiteDataManager

app = Flask(__name__, template_folder="templates")
app.register_blueprint(api, url_prefix='/api')

# Generate a secret key
secret_key = os.urandom(24)  # Generate a 24-byte (192-bit) random key

# Set the secret key
app.secret_key = secret_key

database_path = os.path.abspath('data/moviedb.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
# Initialize the SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)


# HTTP Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Exception Handling
# @app.errorhandler(Exception)
# def handle_exception(e):
#     # Log the exception or perform any other necessary actions
#     return render_template('500.html'), 500


@app.route('/users')
def list_users():
    """
    Lists all the users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route for adding a new user.
    If a POST request is received, validates the form input and adds the user to the data.
    Redirects to the user_movies route for the newly added user.
    If a GET request is received, renders the add_user.html template.
    """
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        # Validate form input as needed

        user_id = data_manager.add_user(name, age)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return render_template('add_users.html')


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Displays the movies for a specific user.
    """
    user = data_manager.get_user(user_id)
    if user is None:
        # Handle non-existing user ID
        return "User not found"

    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
     Route for adding a new movie for a specific user.

     If a POST request is received, validates the form input and adds the movie to the user's list of favorite movies.
     Redirects to the user's movies page after adding the movie.

     If a GET request is received, renders the add_movie.html template.
     """
    user = data_manager.get_user(user_id)
    if user is None:
        # Handle non-existing user ID
        return "User not found"

    if request.method == 'POST':
        # Handle form submission
        title = request.form['title']
        director = request.form['director']
        year = int(request.form['year'])
        rating = float(request.form['rating'])

        # Check if the movie name already exists for the user
        movies = data_manager.get_user_movies(user_id)  # Get the list of movies
        if any(movie.title == title for movie in movies):
            return "Movie with the same name already exists for the user"

        # Process the form data and add the movie to the user's list of favorite movies
        data_manager.add_user_movie(user_id, title, director, year, rating)

        # Redirect to the user's movies page
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        # Display the add movie form
        return render_template('add_movies.html', user=user, user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route for updating a movie for a specific user.
    If a POST request is received, updates the movie details.
    Redirects to the user's movies page after updating the movie.
    If a GET request is received, renders the update_movie.html template with pre-filled movie details.
    """
    user = data_manager.get_user(user_id)
    if user is None:
        # Handle non-existing user ID
        return "User not found"

    movie = data_manager.get_movie(movie_id)  # Replace this with the appropriate method to retrieve a movie
    if movie is None:
        # Handle non-existing movie ID
        return "Movie not found"

    if request.method == 'POST':
        # Handle form submission
        movie['name'] = request.form['title']
        movie['director'] = request.form['director']
        movie['year'] = int(request.form['year'])
        movie['rating'] = float(request.form['rating'])

        # Process the form data and update the movie details
        data_manager.update_user_movie(user_id, movie_id, movie['name'], movie['director'], movie['year'],
                                       movie['rating'])

        # Redirect to the user's movies page after updating the movie
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        # Display the update movie form pre-filled with the current movie details
        return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """
    Route for deleting a movie from a user's list of movies.
    If a POST request is received, deletes the movie from the user's list of movies.
    Redirects to the user's movies page after deleting the movie.
    """
    user = data_manager.get_user(user_id)
    if user is None:
        # Handle non-existing user ID
        return "User not found"

    # Delete the movie from the user's list of movies
    success = data_manager.delete_user_movie(user_id, movie_id)
    if not success:
        # Handle non-existing movie ID
        return "Movie not found"

    # Redirect to the user's movies page after deleting the movie
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/add_review/<int:movie_id>', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']

        if not review_text or not rating:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('add_review', user_id=user_id, movie_id=movie_id))

        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError()
        except ValueError:
            flash('Invalid rating value. Please enter a number between 0 and 10.', 'error')
            return redirect(url_for('add_review', user_id=user_id, movie_id=movie_id))

        # Validation successful, proceed to add the review
        data_manager.add_review(user_id, movie_id, review_text, rating)
        flash('Review added successfully.', 'success')
        return redirect(url_for('movie_reviews', user_id=user_id, movie_id=movie_id))

    else:
        user = data_manager.get_user(user_id)
        movie = data_manager.get_movie(movie_id)
        return render_template('add_review.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/movie_reviews/<int:movie_id>')
def movie_reviews(user_id, movie_id):
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)
    reviews = data_manager.get_movie_reviews(movie_id)

    return render_template('movie_reviews.html', user=user, movie=movie, reviews=reviews)


@app.route('/')
def home():
    return "Welcome to Movie Database"


if __name__ == '__main__':
    app.run(debug=True)