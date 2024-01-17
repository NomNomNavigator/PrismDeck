from flask import Blueprint, render_template, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from flask_login import current_user, login_required
from .models import MovieRating, Movie
from . import

rec = Blueprint('rec', __name__)


@rec.route('/rec', methods=['GET'])
@login_required
def recommendation():
    # Starting spark session
    spark = SparkSession.builder \
        .appName("PrismDeck") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

    # # loading in the trained ALS rating model
    # rating_model = ALSModel.load('/Users/imir/python/rating_model')
    # # Querying the user from the database
    # user_id = current_user.id
    # user_rating = MovieRating.query.filter_by(user_id=user_id).all()
    #
    # # Create a DataFrame with user ratings
    # user_ratings_data = [(rating.movie_id, rating.rating) for rating in user_rating]
    # user_df = spark.createDataFrame(user_ratings_data, ['userId', 'movieId', 'rating'])
    #
    # # Get recommendations for the user
    # num_rec = 5
    # # user_df = spark.createDataFrame([(user_id,)], ['userId'])
    # recommendations = rating_model.recommendForUserSubset(user_df, num_rec)
    #
    # # Extract movie IDs from recommendations
    # recommended_movie_ids = [row.movieId for row in recommendations.select("movieId").collect()]
    #
    # # Fetch movie details for the recommended movies
    # recommended_movies = Movie.query.filter(Movie.id.in_(recommended_movie_ids)).all()
    #
    # # Stop the spark session
    # spark.stop()
    # return render_template('/recommendation.html', rec_movie=recommended_movies)


# Route to use the model for movie recommendation
@rec.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # To load my ALS Model
    als_model_path = "/Users/joey/Downloads/model_training"
    als_model = ALSModel.load(als_model_path)

    try:
        spark = SparkSession.builder.appName("PrismDeck").getOrCreate()
        # Extract user ID from the request data
        user_id = request.json['user_id']

        # Use ALS model to generate recommendations for the specified user
        user_recommendations = als_model.recommendForUserSubset(spark.createDataFrame([(user_id,)]), 10)

        # Convert the recommendations to a JSON response
        result = user_recommendations.toJSON().collect()

        return jsonify({'recommendations': result})
    except Exception as e:
        return jsonify({'error': str(e)})
