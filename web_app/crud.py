"""
CRUD Functions for interacting with tables/data via the ORM
"""
from .models import Movie, MovieRating, User, UserMixin, MovieGenre
from sqlalchemy import select, update, desc, and_, case, func
from sqlalchemy.exc import SQLAlchemyError
from . import db
from flask_login import current_user


# Checking if the user has rated this movie before
def check_previous_rating(usr_id: int, movie_id: int):
    result = db.session.execute(select(MovieRating.movie_id).where(
        and_(MovieRating.user_id == usr_id, MovieRating.movie_id == movie_id))).first()

    if result:
        db_movie_id = int(result[0])
        if db_movie_id == movie_id:
            return True
        else:
            return False
    else:
        return False


# The first time a user rates a movie, save a new record to movie_rating table
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


# When a user re-rates an already rated movie, update the existing record with the new rating
def update_movie_rating(usr_id: int, movie_id: int, rating: float):
    try:
        # Seems either could work, pick one or the other
        movie_rating = MovieRating.query.filter_by(user_id=usr_id, movie_id=movie_id).first()
        # movie_rating2 = db.session.execute(select(MovieRating.movie_id).where(MovieRating.user_id == usr_id)).fetchall()

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


# Not being used currently, only grabbing fav_genres for the rate_movies page
def get_user_preferences(usr_id: int):
    fav_genres = get_user_fav_genres(usr_id)
    fav_movies = get_user_fav_movies(usr_id)
    return fav_genres, fav_movies


# Get a users favorite movie genres (3 max, 3 enforced currently)
def get_user_fav_genres(usr_id: int):
    ug_result = db.session.execute(select(User.fav_genre1, User.fav_genre2, User.fav_genre3)
                                   .where(User.id == usr_id)).first()
    if ug_result:
        user_genres = [genre.lower() for genre in ug_result]
        return user_genres
    else:
        return None


# Get a users favorite movies (3 max, 3 enforced currently)
def get_user_fav_movies(usr_id: int):
    um_result = db.session.execute(select(User.fav_mov1, User.fav_mov2, User.fav_mov3)
                                   .where(User.id == usr_id)).first()
    if um_result:
        user_movies = [mov for mov in um_result]
        return user_movies
    else:
        return None


# Get all the movies a user has rated (each row is a dict, i think, need to test)
def get_user_rated_movies(usr_id: int):
    urm_result = db.session.execute(select(MovieRating.movie_id)
                                   .where(MovieRating.user_id == usr_id)).fetchall()
    if urm_result:
        user_rated_movies = [mov[0] for mov in urm_result]
        return user_rated_movies
    else:
        return []


# Get movies to rate, ordered by unrated movies matching fav genres that are highest rated (Faster to make query do it?)
def get_movies_to_rate(fav_genres):
    usr_id = current_user.id

    # Trying to make a subquery to get genre match to fav genres count, making the count a column wasn't working for cases
    matching_genres_sq = select(
        MovieGenre.movie_id,
        func.count(MovieGenre.id).label('matching_genre_count')
    ).where(
        MovieGenre.genre.in_(fav_genres)
    ).group_by(
        MovieGenre.movie_id
    ).subquery()

    # Now put the subquery in the main query as a column
    query = select(
        Movie.id,
        Movie.title,
        Movie.year,
        Movie.avg_rate,
        matching_genres_sq.c.matching_genre_count,
        Movie.total_ratings
    ).select_from(
        Movie.__table__.join(
            matching_genres_sq,
            Movie.id == matching_genres_sq.c.movie_id,
            isouter=True
    )).where(
        Movie.id.notin_(select(MovieRating.movie_id).where(MovieRating.user_id == usr_id))
    ).order_by(
        case(
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 5000), 0),
            (and_(Movie.avg_rate.between(4.1, 4.5), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 5000), 1),
            (and_(Movie.avg_rate.between(3.6, 4.0), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 5000), 2),
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count >= 1, Movie.total_ratings >= 5000), 3),
            (and_(Movie.avg_rate.between(4.1, 4.5), matching_genres_sq.c.matching_genre_count >= 1, Movie.total_ratings >= 5000), 4),
            (and_(Movie.avg_rate.between(3.6, 4.0), matching_genres_sq.c.matching_genre_count >= 1, Movie.total_ratings >= 5000), 5),
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 1000), 6),
            (and_(Movie.avg_rate.between(4.1, 4.5), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 1000), 7),
            (and_(Movie.avg_rate.between(3.6, 4.0), matching_genres_sq.c.matching_genre_count >= 2, Movie.total_ratings >= 1000), 8),
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count == 1, Movie.total_ratings >= 1000), 9),
            (and_(Movie.avg_rate.between(4.0, 4.5), matching_genres_sq.c.matching_genre_count == 1, Movie.total_ratings >= 1000), 10),
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count == 0, Movie.total_ratings >= 5000), 11),
            (and_(Movie.avg_rate.between(4.0, 4.5), matching_genres_sq.c.matching_genre_count == 0, Movie.total_ratings >= 5000), 12),
            (and_(Movie.avg_rate.between(4.6, 5.0), matching_genres_sq.c.matching_genre_count == 0, Movie.total_ratings >= 200), 13),
            (and_(Movie.avg_rate.between(4.0, 4.5), matching_genres_sq.c.matching_genre_count == 0, Movie.total_ratings >= 200), 14),
            (and_(Movie.avg_rate.between(3.0, 3.9), matching_genres_sq.c.matching_genre_count >= 1, Movie.total_ratings >= 200), 15),
            (and_(Movie.avg_rate.between(3.0, 5.0), matching_genres_sq.c.matching_genre_count >= 1, Movie.total_ratings < 200), 16),
            else_=17),
        desc(Movie.avg_rate)
    )

    result = db.session.execute(query)

    # Fetch and return the results
    movies_to_rate = []
    for row in result:
        movies_to_rate.append({
            'id': row[0],
            'title': row[1],
            'year': row[2],
            'avg_rate': row[3],
            'rates': row[5]
        })
    print(movies_to_rate[0])
    return movies_to_rate


# This was too slow at returning movies, googled and querying to DB handling match and order can be faster
# def get_movies_to_rate(rated_movies: list, fav_genres: list):
#
#     movie_list = Movie.query.order_by(desc(Movie.avg_rate)).limit(200).all()
#
#     if movie_list:
#         # movies = [mov for mov in movie_list]
#         # return movies
#         movies = []
#         user_rated_movies = []
#         for mov in movie_list:
#             if mov.id not in rated_movies:
#                 movies.append(mov)
#             else:
#                 user_rated_movies.append(mov)
#         # Get count of unrated movies genres matched to fav_genres
#         for m in movies:
#             m.genre_count = 0
#             for g in m.genres:
#                 if g.genre in fav_genres:
#                     m.genre_count += 1
#         # Get count of user rated movies genres matched to fav_genres
#         for mv in user_rated_movies:
#             mv.genre_count = 0
#             for g in mv.genres:
#                 if g.genre in fav_genres:
#                     mv.genre_count += 1
#
#         # Sort by fav_genres matches, then the movies average rating
#         # Not sure if I'm even using lambda properly in the key, hoping it orders by genre count then avg rating
#         sorted_movies = sorted(movies, key=lambda mo: (mo.genre_count, mo.avg_rate), reverse=True)
#         sorted_rated_movies = sorted(user_rated_movies, key=lambda mo: (mo.genre_count, mo.avg_rate), reverse=True)
#         # Order by unrated movies, then rated movies
#         return sorted_movies + sorted_rated_movies
#     else:
#         raise Exception("Error retrieving movies to rate")


# def get_movies_to_rate(fav_genres):
#     usr_id = current_user.id
#
#     # Want to show the user the movie title, year, average rating and total ratings.
#     query = select(
#         Movie.id,
#         Movie.title,
#         Movie.year,
#         Movie.avg_rate,
#         func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)).label('matching_genre_count'),
#         Movie.total_ratings
#     ).select_from(
#         # Joining movies and movie genres, need the genres to create the genre match count and track for each movie
#         Movie.__table__.join(MovieGenre, Movie.id == MovieGenre.movie_id, isouter=True)
#     ).where(
#         # Using subquery to filter out movies the user already rated
#         Movie.id.notin_(select(MovieRating.movie_id).where(MovieRating.user_id == usr_id))
#     ).group_by(
#         # Need the group_by on movie id for the count to be aggregated to the movie
#         Movie.id
#     ).order_by(
#         case(
#               #  Can't get this to work, need to consider the matched fav genres count for the case but can't use func or a calc column
#             (and_(Movie.avg_rate.between(4.6, 5.0), matching_genre_count >= 2, Movie.total_ratings >= 200), 0),
#             (and_(Movie.avg_rate.between(4.0, 4.5), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) >= 2, Movie.total_ratings >= 200), 1),
#             (and_(Movie.avg_rate.between(4.6, 5.0), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) == 1, Movie.total_ratings >= 200), 2),
#             (and_(Movie.avg_rate.between(4.0, 4.5), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) == 1, Movie.total_ratings >= 200), 3),
#             (and_(Movie.avg_rate.between(4.6, 5.0), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) == 0, Movie.total_ratings >= 200), 4),
#             (and_(Movie.avg_rate.between(4.0, 4.5), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) == 0, Movie.total_ratings >= 200), 5),
#             (and_(Movie.avg_rate.between(3.0, 3.9), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) >= 1, Movie.total_ratings >= 200), 6),
#             (and_(Movie.avg_rate.between(3.0, 5.0), func.count(MovieGenre.id).filter(MovieGenre.genre.in_(fav_genres)) >= 1, Movie.total_ratings < 200), 7),
#             else_=8),
#         # Order movies in each case rank from highest rank to lowest
#         desc(Movie.avg_rate)
#     )
#
#     result = db.session.execute(query)
#
#     # Fetch and return the results
#     movies_to_rate = []
#     for row in result:
#         movies_to_rate.append({
#             'id': row[0],
#             'title': row[1],
#             'year': row[2],
#             'avg_rate': row[3],
#             'rates': row[5]
#         })
#     print(movies_to_rate[0])
#     return movies_to_rate



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
