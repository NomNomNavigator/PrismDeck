from flask import Blueprint, render_template, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from flask_login import current_user, login_required
from .models import MovieRating, Movie
from .recommendation_model import load_als_model, get_recommendations


rec = Blueprint('rec', __name__)

@rec.route('/get_recommendations', methods=['POST'])
