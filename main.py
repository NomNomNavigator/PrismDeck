from web_app import create_app, db, ssh_tunnel
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

# Initialize the database
with app.app_context():
    db.create_all()

# will only run the web server in this file
if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        ssh_tunnel.stop()
