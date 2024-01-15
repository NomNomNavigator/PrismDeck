from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .crud import (save_movie_rating, get_user_rated_movies, get_user_fav_genres, get_movies_to_rate,
                   check_previous_rating, update_movie_rating)


rate_movies = Blueprint('rate_movies', __name__)
current_movie_position = 0
cached_movies = None


# Route for rating movies, two routes will call this endpoint (prefer, home)
@rate_movies.route('/rate-movies', methods=['GET'])
@login_required
def get_movies():
    global current_movie_position, cached_movies

    usr_id = current_user.id

    if cached_movies is None:
        user_fav_genres = get_user_fav_genres(usr_id)
        user_rated_movies = get_user_rated_movies(usr_id)
        movies = get_movies_to_rate(user_rated_movies, user_fav_genres)
        cached_movies = movies
    else:
        movies = cached_movies

    # Slice the list to get the next 8 movies starting from the current position
    movies_to_rate = movies[current_movie_position : current_movie_position + 8]

    return render_template('rate-movies.html', user=current_user, movies=movies_to_rate)


# Route for posting movie rating movies
# Note:  Most likely need to change dict to whatever type is going to be passed in from client
@rate_movies.route('/rate-movies', methods=['POST'])
@login_required
def rate_movie():
    global current_movie_position, cached_movies
    user_id = current_user.id
    movie_ids = request.form.getlist('movie_ids[]')

    for movie in movie_ids:
        movie_id = int(movie)
        rating = int(request.form.get(f'rating_{movie}', -1))

        if rating != -1:
            prev_rated = check_previous_rating(user_id, movie_id)
            if prev_rated:
                update_movie_rating(user_id, movie_id, rating)
            else:
                save_movie_rating(user_id, movie_id, rating)

    # Add 10 to counter get next 10 movies if "next" is clicked
    current_movie_position += 8

    if current_movie_position >= 192:
        current_movie_position = 0

    if 'next' in request.form:
        return redirect(url_for('rate_movies.get_movies'))
    elif 'finish' in request.form:
        current_movie_position = 0
        cached_movies = None
        return redirect(url_for('views.access'))
