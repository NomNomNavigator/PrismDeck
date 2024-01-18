from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Movie, db

views = Blueprint('views', __name__)


# route for users that are not yet logged in or who have not signed up
@views.route('/')
def access():
    return render_template('index.html')


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
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"
]

user_genres = []


# home page of the users that are logged in
@views.route('/prefer', methods=['POST', 'GET'])
@login_required
def prefer():
    if request.method == 'POST':
        fav_mov1 = request.form.get('fav_mov1')
        fav_mov2 = request.form.get('fav_mov2')
        fav_mov3 = request.form.get('fav_mov3')
        fav_genre1 = request.form.get('fav_genre1')
        fav_genre2 = request.form.get('fav_genre2')
        fav_genre3 = request.form.get('fav_genre3')

        movie1 = Movie.query.filter_by(title=fav_mov1).first()
        movie2 = Movie.query.filter_by(title=fav_mov2).first()
        movie3 = Movie.query.filter_by(title=fav_mov3).first()

        # genre1 = MovieGenre.query.filter_by(genre=fav_genre1)
        # genre2 = MovieGenre.query.filter_by(genre=fav_genre2)
        # genre3 = MovieGenre.query.filter_by(genre=fav_genre3)
        # Checking to see if the movie the user inputted is in the database
        if movie1 is None:
            flash("Sorry, the first movie you entered is not in our registry, please try typing a different movie",
                  category='error')
        elif movie2 is None:
            flash("Sorry, the second movie you entered is not in our registry, please try typing a different movie",
                  category='error')
        elif movie3 is None:
            flash("Sorry, the third movie you entered is not in our registry, please try typing a different movie",
                  category='error')
        # Checking if the genre the user entered is in the database
        elif fav_genre1 not in genres:
            flash("Your first entry for favorite genres does not exists in our records. please select another genre",
                  category='error')
        elif fav_genre2 not in genres:
            flash("Your second entry for favorite genres does not exists in our records. please select another genre",
                  category='error')
        elif fav_genre3 not in genres:
            flash("Your third entry for favorite genres does not exists in our records. please select another genre",
                  category='error')
        # User inputs values in the database, their values will be loaded to the database
        else:
            current_user.fav_mov1 = movie1.id
            current_user.fav_mov2 = movie2.id
            current_user.fav_mov3 = movie3.id
            current_user.fav_genre1 = fav_genre1
            current_user.fav_genre2 = fav_genre2
            current_user.fav_genre3 = fav_genre3
            db.session.commit()
            flash("Your preferences have been successfully saved to your profile!", category="success")
            return redirect(url_for('rate_movies.get_movies'))
    return render_template('prefer.html', user=current_user)


@views.route('/prism-home', methods=['POST', 'GET'])
@login_required
def home():
    # The model would be a pickle file, which would be read at app creation

    # POST, the info the model needs? I assume the movies the user has rated?

    # What does the model give back? Movie ids?

    return render_template('prism-home.html', user=current_user,)
