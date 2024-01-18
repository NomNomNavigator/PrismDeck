from flask import Blueprint, render_template
from flask_login import login_required, current_user

head_shots = Blueprint('head_shot', __name__)


@head_shots.route('/head_shots')
def hire_us():
    return render_template('head_shots.html', user=current_user)
