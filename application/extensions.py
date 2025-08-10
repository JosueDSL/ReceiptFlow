# Description: This file initializes the extensions used in the application.

# Import the required modules
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


# Initialize the extensions

# JWTManager is used to manage the JWT tokens for the application.
jwt = JWTManager()

# Migrate is used to manage the database migrations.
migrate = Migrate()