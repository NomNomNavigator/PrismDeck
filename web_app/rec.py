from pyspark.sql.functions import explode
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from flask_login import current_user, login_required
from .models import MovieRating, Movie
from flask import Blueprint, render_template


rec = Blueprint('rec', __name__)


@rec.route('/rec', methods=['GET'])
@login_required
def recommendation():
    # Checking if the user's ID is in the model
    user_id = current_user.id
    if user_id < 162541:
        # Starting spark session
        spark = SparkSession.builder \
            .appName("PrismDeck") \
            .config("spark.driver.memory", "4g") \
            .getOrCreate()

        # loading in the trained ALS rating model
        rating_model = ALSModel.load('web_app/model/rating_model_file copy')

        user_id = current_user.id
        # Querying the database for the user's rated movies
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

        # Stopping the spark session
        spark.stop()
        return render_template('/recommendation.html', user=current_user, rec_movie=recommended_movies)

