from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from crud import save_movie_rating, get_user_rated_movies, get_user_preferences, get_movies_to_rate

rate_movies = Blueprint('rate_movies', __name__)


# Route for rating movies, two routes will call this endpoint (prefer, home)
@rate_movies.route('/rate-movies', methods=['GET'])
@login_required
def get_movies(usr_id: int):
    user_preferences = get_user_preferences(usr_id)
    user_rated_movies = get_user_rated_movies(usr_id)
    movies_to_rate = get_movies_to_rate(user_rated_movies, user_preferences)
    return render_template('rate-movies.html', user=current_user)


# Route for posting movie rating movies
# Note:  Most likely need to change dict to whatever type is going to be passed in from client
@rate_movies.route('/rate-movies', methods=['POST'])
@login_required
def rate_movies(usr_id: int, movie_ratings: dict):
    try:
        is_five = len(movie_ratings)
        if is_five < 5:
            for movie in movie_ratings:
                movie_id = movie.id
                rating = movie.rating
                save_movie_rating(usr_id, movie_id, rating)
            return render_template('prism-home.html', user=current_user)
    except ValueError:
        return "Must rate at least 5 movies"
