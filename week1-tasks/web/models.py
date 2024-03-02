from sqlalchemy.sql import func
from . import db

class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        date_created (datetime): The date and time when the user was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
