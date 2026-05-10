from flask_sqlalchemy import SQLAlchemy

# Shared database object for the backend

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
