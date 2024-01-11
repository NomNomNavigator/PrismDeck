from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import User, Movie

views = Blueprint('views', __name__)


# route for users that are not yet logged in or who have not signed up
@views.route('/')
def access():
    return render_template('index.html')


# home page of the users that are logged in
@views.route('/prefer', methods=['POST', 'GET'])
# @login_required
def prefer():

    if request.method == 'POST':
        fav_movie1 = request.form.get('fav_movie1')
        fav_movie2 = request.form.get('fav_movie2')
        fav_movie3 = request.form.get('fav_movie3')
        fav_genre1 = request.form.get('fav_genre1')
        fav_genre2 = request.form.get('fav_genre2')
        fav_genre3 = request.form.get('fav_genre')

        if Movie.query.filter_by(title=fav_movie1).first() is None:
            flash("Sorry, that movie is not in our registry, please try typing a different movie")

    return render_template('prefer.html', user=current_user)
