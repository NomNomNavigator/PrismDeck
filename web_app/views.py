from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


# route for users that are not yet logged in or who have not signed up
@views.route('/')
def access():
    return render_template('index.html')


# home page of the users that are logged in
@views.route('/prefer', methods=['POST', 'GET'])
# @login_required
def prefer():
    return render_template('prefer.html', user=current_user)
