"""
CRUD Functions for interacting with tables/data via the ORM
"""
from .models import Movie, MovieRating, User, UserMixin
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from . import db


def check_previous_rating(usr_id: int, movie_id: int):
    result = db.session.execute(select(MovieRating.movie_id)
                                .where(MovieRating.user_id == usr_id)).first()
    if result:
        db_movie_id = int(result.movie_id)
        if db_movie_id == movie_id:
            return True
        else:
            return False
    else:
        return False


# This may need to be a route of some sort in order for JS or JS Ajax to save ratings as they happen.
def save_movie_rating(usr_id: int, movie_id: int, rating: float):
    try:
        movie_rating = MovieRating(
            user_id=usr_id,
            movie_id=movie_id,
            rating=rating
        )
        db.session.add(movie_rating)
        db.session.commit()
        return "Success"
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error saving moving rating: {str(e)}"


# This may need to be a route of some sort in order for JS or JS Ajax to save ratings as they happen.
def update_movie_rating(usr_id: int, movie_id: int, rating: float):
    try:
        # I don't understand which way will work / is better.
        movie_rating = MovieRating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        movie_rating2 = db.session.execute(select(MovieRating.movie_id).where(MovieRating.user_id == usr_id)).fetchall()

        if movie_rating:
            movie_rating.rating = rating
            # update_rating = db.session.execute(
            #   update(MovieRating).where(user_id=user_id, movie_id=movie_id).values(rating=rating))
            db.session.commit()
            return "Success"
        else:
            return "Movie rating not found for the given user and movie ID."

    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error updating movie rating: {str(e)}"



def get_user_preferences(usr_id: int):
    fav_genres = get_user_fav_genres(usr_id)
    fav_movies = get_user_fav_movies(usr_id)
    return fav_genres, fav_movies


def get_user_fav_genres(usr_id: int):
    ug_result = db.session.execute(select(User.fav_genre1, User.fav_genre2, User.fav_genre3)
                                   .where(User.id == usr_id)).first()
    if ug_result:
        user_genres = [genre for genre in ug_result]
        return user_genres
    else:
        return None


def get_user_fav_movies(usr_id: int):
    um_result = db.session.execute(select(User.fav_mov1, User.fav_mov2, User.fav_mov3)
                                   .where(User.id == usr_id)).first()
    if um_result:
        user_movies = [mov for mov in um_result]
        return user_movies
    else:
        return None


def get_user_rated_movies(usr_id: int):
    urm_result = db.session.execute(select(MovieRating.movie_id)
                                   .where(MovieRating.user_id == usr_id)).fetchall()
    if urm_result:
        user_rated_movies = [mov for mov in urm_result]
        return user_rated_movies
    else:
        return None


def get_movies_to_rate(rated_movies: list, usr_prefs: list):

    pass


# Function to get the valid genre strings
def get_genres()-> list:
    genres = [
        "Action",
        "Adventure",
        "Animation",
        "Children's",
        "Comedy",
        "Crime",
        "Documentary",
        "Drama",
        "Fantasy",
        "Film-Noir"
        "Horror",
        "Musical",
        "Mystery",
        "Romance",
        "Sci-Fi",
        "Thriller",
        "War",
        "Western"
    ]
    return genres


# Function to get the movie links to display on a tile
# Alt Ideas:  Accept 3 movie_ids, break out functions to get link for either of the sites
def get_movie_links(movie_id: int) -> list:

    movie_link_ids = db.session.execute(select(Movie.imdb_id, Movie.tmdb_id).where(Movie.id == movie_id)).first()
    if movie_link_ids:
        imdb_id, tmdb_id = movie_link_ids
        imdb_link = f"http://www.imdb.com/title/{imdb_id}/"
        tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}"
        movie_link_list = [ imdb_link, tmdb_link ]
        return movie_link_list
    else:
        raise Exception("Error retrieving movie links")


def save_movie_tag(user_id, movie_id, tag):
    pass