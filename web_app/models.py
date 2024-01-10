"""
ORM using SQLAlchemy for our project.  Based on the Data Model we design, will update as we learn

It seems there are multiple ways to have SQLAlchemy create the DB tables and implement the model.
1. [SELECTED] Using Model directly - direct model referencing (this seems to be an older style, but popular still)
2. Using DeclarativeBase - seems to be preferred way to use SQLAlchemy these days, slight changes
"""
import datetime
from flask_login import UserMixin
from . import db
# Below For sqlalchemy 3.0 approach with Base model
# from sqlalchemy import Column, Integer, String, Float


# For user sign-up, login, session tracking, preferences, feedback tracking
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    # The data below is used to capture preferences explicitly, and evals/feedback from recos
    fav_restaurant = db.Column(db.Integer)
    least_fav_restaurant = db.Column(db.Integer)
    pref_ambiance = db.Column(db.String(100))
    pref_cuisine = db.Column(db.String(100))
    pref_price_range = db.Column(db.String(100))
    pos_restaurants = db.Column(db.Text)
    neg_restaurants = db.Column(db.Text)
    home_city = db.Column(db.String(50))
    home_state = db.Column(db.String(2))

# For tracking a profile capturing user preferences, and feedback as they use the site
# class UserProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     fav_restaurant = db.Column(db.Integer)
#     least_fav_restaurant = db.Column(db.Integer)
#     pref_ambiance = db.Column(db.Text)
#     pref_cuisine = db.Column(db.Text)
#     pref_price_range =  db.Column(db.Text)
#     pos_restaurants = db.Column(db.Text)
#     neg_restaurants = db.Column(db.Text)
#     home_city = db.Column(db.Text)
#     home_state = db.Column(db.Text)


# For restaurants to prefer, rate and recommend
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yelp_id = db.Column(db.String(60), unique=True)
    name = db.Column(db.String(60), nullable=False)
    avg_rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    price_range = db.Column(db.String(4))
    site_url = db.Column(db.String(100))
    image_url = db.Column(db.Text)
    d_address = db.Column(db.String(300), nullable=False)
    phone_num = db.Column(db.String(20))
    is_closed = db.Column(db.Boolean, default=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)


# For categories that apply to a restaurant from source data - 0 to Many it seems
class RestaurantCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.String(60), db.ForeignKey('restaurant.yelp_id'), nullable=False)
    category = db.Column(db.String(50))
    alias = db.Column(db.String(50))
    # Initial app won't use type for simplicity sake, making it nullable
    type = db.Column(db.String(30), nullable=True)


# For requests to recommend a restaurant - data input by user, mapped ids and/or from profile if no entry
class RestaurantRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # profile_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'), nullable=False)
    key_restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    request_date = db.Column(db.DateTime)
    # 1 each at most selected of ambiance, cuisine, price_range. Can leave blank, grab from profile if so.
    ambiance = db.Column(db.String(100))
    cuisine = db.Column(db.String(100))
    price_range = db.Column(db.String(4))
    in_city = db.Column(db.String(50))
    in_state = db.Column(db.String(2))


# For recommendations of restaurants - data return to user after request, top 3 restaurants recommended
class RestaurantReco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    # Top 3 Restaurants returned
    reco_one = db.Column(db.Integer, nullable=False)
    reco_two = db.Column(db.Integer)
    reco_three = db.Column(db.Integer)
    reco_timestamp = db.Column(db.DateTime, nullable=False)
    # Captures result of prompting user for "Where did you eat?" or something like that
    reco_taken = db.Column(db.Boolean, nullable=True)
    picked_reco = db.Column(db.Integer, nullable=True)
    picked_reco_eval = db.Column(db.String(1), nullable=True)
    eval_timestamp = db.Column(db.DateTime, nullable=True)
