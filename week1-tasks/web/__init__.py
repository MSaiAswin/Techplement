from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    from .models import User

    with app.app_context():
        create_database(db)

    return app

def create_database(db):
    """
    Creates the database if it does not exist.

    Args:
        db (SQLAlchemy): The SQLAlchemy instance.

    Returns:
        None
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')
