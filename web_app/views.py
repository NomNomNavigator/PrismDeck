from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import User, Movie, MovieGenre

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
        fav_mov1 = request.form.get('fav_mov1')
        fav_mov2 = request.form.get('fav_mov2')
        fav_mov3 = request.form.get('fav_mov3')
        fav_genre1 = request.form.get('fav_genre1')
        fav_genre2 = request.form.get('fav_genre2')
        fav_genre3 = request.form.get('fav_genre')

        # checking to see if the movie the user inputted is in the database
        if Movie.query.filter_by(title=fav_mov1).first() is None:
            flash("Sorry, the first movie you entered is not in our registry, please try typing a different movie")
        elif Movie.query.filter_by(title=fav_mov2).first() is None:
            flash("Sorry, the second movie you entered is not in our registry, please try typing a different movie")
        elif Movie.query.filter_by(title=fav_mov3).first() is None:
            flash("Sorry, the third movie you entered is not in our registry, please try typing a different movie")
        elif MovieGenre.query.filter_by(genre=fav_genre1) is None:
            flash("Your first entry for favorite genres does not exists in our records. please select another genre")
        elif MovieGenre.query.filter_by(genre=fav_genre2) is None:
            flash("Your second entry for favorite genres does not exists in our records. please select another genre")
        elif MovieGenre.query.filter_by(genre=fav_genre3) is None:
            flash("Your third entry for favorite genres does not exists in our records. please select another genre")
        else:
            new_user_fav = User.query.update()
    return render_template('prefer.html', user=current_user)
