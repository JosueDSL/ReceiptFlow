# Description: Configuration file for the Flask application.
# NOTE: The only configuration implemented is for the development environment. The production configuration is not implemented for this test.

# Import the required modules
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Configuration base class for the Flask application
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=4)
    JWT_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
    JWT_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    JWT_COOKIE_HTTPONLY = False
    JWT_CSRF_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    AZURE_FUNCTION_URL = os.environ.get('AZURE_FUNCTION_URL', 'http://localhost:7071/api/get-news-data?')

    # Print config
    def __repr__(self) -> str:
        return f"Config({self.__dict__})"


# Base class configuration for the development environment
class BaseDevelopmentConfig(Config):
    # Enable debug mode
    DEBUG = True

    # Set the base directory to the current directory of flask-backend
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Enable SQLALCHEMY_ECHO to print SQL queries
    # SQLALCHEMY_ECHO = True


# Configuration for the development environment
class DevelopmentConfig(BaseDevelopmentConfig):
    # SQLite database URI set to root level of flask-backend
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or f"postgresql://{os.path.join(BaseDevelopmentConfig.BASE_DIR, 'receiptflow.db')}"



# Configuration for the Docker development environment
class DevelopmentDockerConfig(BaseDevelopmentConfig):

    # SQLite database URI set to root level of /app inside the container
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_DOCKER_URL') or f"postgresql://{os.path.join(BaseDevelopmentConfig.BASE_DIR, 'receiptflow.db')}"