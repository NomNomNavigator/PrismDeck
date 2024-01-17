from pyspark.sql.functions import explode
from pyspark.ml.recommendation import ALS, ALSModel
from flask_login import current_user, login_required
from .models import MovieRating, Movie, MovieGenre
from . import db
from collections import defaultdict
from sqlalchemy.orm import aliased


rec = Blueprint('rec', __name__)



def get_all_movies_with_genres():
    # Aliasing to handle self-referential join (if necessary)
    genre_alias = aliased(MovieGenre)

    # Query to get movies and their genres
    movies = db.session.query(
        Movie.id,
        Movie.avg_rate,
        Movie.total_ratings,
        db.func.group_concat(genre_alias.genre).label('genres')
    ).join(
        genre_alias, Movie.id == genre_alias.movie_id, isouter=True
    ).group_by(
        Movie.id
    ).all()

    # Convert results to a dictionary format
    all_movies = {
        movie.id: {
            'avg_rate': movie.avg_rate,
            'total_ratings': movie.total_ratings,
            'genres': movie.genres.split(',') if movie.genres else []
        } for movie in movies
    }
    return all_movies


@rec.route('/rec', methods=['GET'])
@login_required
def recommendation():
    user_id = current_user.id
    if user_id < 162541:
        # Starting spark session
        spark = SparkSession.builder \
            .appName("PrismDeck") \
            .config("spark.driver.memory", "4g") \
            .getOrCreate()

        # loading in the trained ALS rating model
        rating_model = ALSModel.load('/Users/mike/Documents/rating_model_file copy')
        # Querying the user from the database
        user_id = current_user.id
        user_rating = MovieRating.query.filter_by(user_id=user_id).all()

        # Create a DataFrame with user ratings
        user_ratings_data = [(rating.user_id, rating.movie_id, rating.rating) for rating in user_rating]
        user_df = spark.createDataFrame(user_ratings_data, ['userId', 'movieId', 'rating'])
        user_df.show()

        # Get recommendations for the user
        num_rec = 5
        # user_df = spark.createDataFrame([(user_id,)], ['userId'])
        recommendations = rating_model.recommendForUserSubset(user_df, num_rec)
        recommendations.show()

        exploded_recommendations = recommendations.select("userId", explode("recommendations").alias("rec"))
        print("Exploded Recommendations:")
        exploded_recommendations.show()

        # Extract movie IDs from recommendations
        recommended_movie_ids = [row.rec.movieId for row in exploded_recommendations.collect()]
        print("Recommended Movie IDs:", recommended_movie_ids)

        # Fetch movie details for the recommended movies
        recommended_movies = Movie.query.filter(Movie.id.in_(recommended_movie_ids)).all()
        print("Recommended Movies:", recommended_movies)

        # Stop the spark session
        spark.stop()
        return render_template('/recommendation.html', user=current_user, rec_movie=recommended_movies)
    else:
        user_rated_movs = MovieRating.query.filter_by(user_id=user_id).all()
        user_ratings_data = [(rating.movie_id, rating.rating) for rating in user_rated_movs]
        all_movs_genres = get_all_movies_with_genres()

        # Determine user's preferred genres
        preferred_genres = defaultdict(int)
        for movie_id, rating in user_ratings_data:
            if rating >= 4:
                for genre in all_movs_genres[movie_id]['genres']:
                    preferred_genres[genre] += 1

        # Score all movies based on user's preferred genres
        movie_scores = defaultdict(float)
        for movie_id, movie_info in all_movs_genres.items():
            score = 0
            for genre in movie_info['genres']:
                if genre in preferred_genres:
                    score += preferred_genres[genre]

            # Add +5 if the movie has more than 200 reviews
            if movie_info['total_ratings'] and movie_info['total_ratings'] > 200:
                score += 100000

            movie_scores[movie_id] = score

        # Select top N movies
        recommended_movs = sorted(movie_scores, key=movie_scores.get, reverse=True)[:5]

        recommended_movies = [Movie.query.get(movie_id) for movie_id in recommended_movs]

        return render_template('/recommendation.html', user=current_user, rec_movie=recommended_movies)

