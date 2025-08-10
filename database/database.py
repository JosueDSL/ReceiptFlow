# Description: This file initializes the database with the provided app or the current app. It also creates all tables if they don't exist.

# Import the required modules
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Function to initialize the database with the provided app or the current app
def init_db(app=None):
    # If the app is not provided, use the current app
    if app is None:
        app = current_app

    # Initialize the database with the app
    db.init_app(app)

# Create all tables if they don't exist
def create_tables(app):
    # Create tables
    try:
        with app.app_context():
            db.create_all()
    except OperationalError as e:
        app.logger.error("An error occurred: %s", str(e))
        app.logger.error("Please verify your configuration settings:")
        app.logger.error("For Docker development, use: app.config.from_object('DevelopmentDockerConfig')")
        app.logger.error("For local development, use: app.config.from_object('DevelopmentConfig')")
        app.logger.error("Ensure the database path is correctly set in the .env file.")
        exit(1)