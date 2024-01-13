from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sshtunnel import SSHTunnelForwarder
from config1 import *


db = SQLAlchemy()

# Configure the ssh_tunnel which is started in create_app() and closed in main.py
ssh_tunnel = SSHTunnelForwarder(
        (ssh_host, port),  # replace with your SSH server details
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=('localhost', 3306)  # replace with your MySQL server details
    )


# initializing flask
def create_app():
    app = Flask(__name__)

    # Start the SSH tunnel
    ssh_tunnel.start()

    # secure the cookies session data; the secret key for the app
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_username}:{db_password}@localhost:{ssh_tunnel.local_bind_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # letting the database know this is the app we are going to use
    db.init_app(app)
    # importing blueprints
    from .views import views
    from .confirm import confirm
    from .models import User
    from .rate_movies import rate_movies

    # registering the blueprints, making them accessible in the application
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(confirm)
    app.register_blueprint(rate_movies)

    login_manager = LoginManager()
    login_manager.login_view = 'confirm.login'
    login_manager.init_app(app)

    # telling flask how to load a user; looks for primary key to look for user
    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(int(_id))

    return app


# I am not sure if we will need this or not
# def create_database(app):
#     if not path.exists('anime_web/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database~')
