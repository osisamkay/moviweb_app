import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

# Create and configure Flask app
app = Flask(__name__)
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'data', 'moviedb.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define declarative base
Base = db.Model


class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    age = Column(Integer, unique=True, nullable=False)

    favorite_movies = relationship('Movie', secondary='favorites', back_populates='favorited_by')


class Movie(Base):
    """
    Represents a movie in the database.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)
    genre = Column(String)
    director = Column(String)
    year = Column(String)
    rating = Column(Integer)

    favorited_by = relationship('User', secondary='favorites', back_populates='favorite_movies')


class Favorites(Base):
    """
    Represents the favorites relationship between users and movies.
    """
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    favorite_date = Column(Date)


class Review(Base):
    """
    Represents a review of a movie by a user.
    """
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    review_text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship('User')
    movie = relationship('Movie')


# Uncomment the following line to create the tables
# with app.app_context():
#     db.create_all()
