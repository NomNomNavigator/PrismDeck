from web_app import create_app, db, ssh_tunnel
from flask_migrate import Migrate
from load_data import load_movies_data

app = create_app()
migrate = Migrate(app, db)

# Initialize the database
with app.app_context():
    db.create_all()
    # Load
    load_movies_data()

# will only run the web server in this file
if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        ssh_tunnel.stop()
