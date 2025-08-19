# Import the configuration classes from the config module
from config import (
    DevelopmentConfig,
    DevelopmentDockerConfig,
    # ProductionConfig,          # Another config class examples, just for common usage reference:
    # QAConfig
)

# Import main Flask class and necessary extensions
from flask import Flask

# Import the database configuration
from database import init_db, create_tables

# Import the extensions for the app
from application.extensions import jwt, migrate

# Import the CORS module
from flask_cors import CORS

# Import logging
import logging

# Import the models to create the tables
from application.models import User, Receipt, ReceiptItem, Merchant, BankTransaction, Category


def create_app():

    # Create an instance of the Flask application
    app = Flask(__name__)

    """
        NOTE: Change the configuration class to match the desired environment.
        Options:
        - DevelopmentConfig: For local development
        - DevelopmentDockerConfig: For Docker development

        Example:
        app.config.from_object(DevelopmentConfig)  # Use this for local development
        app.config.from_object(DevelopmentDockerConfig)  # Use this for Docker development
    """

    # Load the configuration from the config.py file
    app.config.from_object(DevelopmentConfig)
    # print(app.config)

    # Initialize the database with the newly created app
    init_db(app)
    with app.app_context():
        create_tables(app)

    # Initialize the migration extension
    # Import the db object from the application module
    from database import db

    migrate.init_app(app, db)

    # Initialize objects of the extensions
    jwt.init_app(app)

    # Configure CORS to allow requests from any origin
    CORS(app, supports_credentials=True, origins=["http://front-end-url-if-apply", "http://localhost:5000"], allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN", "x-api-key"], expose_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN", "x-api-key"])

    # Import the blueprints
    from .blueprints import auth_bp, receipt_bp

    # Register the blueprints with url prefixes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(receipt_bp, url_prefix='/receipts')

    # Import the function here to avoid circular import
    from database import StartupSeeder

    # Run the function once initially, to seed the database
    table = StartupSeeder(app)
    table.seed()


    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('app.log'),
                            logging.StreamHandler()
                        ])
    
    # Set the logging level for httpcore and httpx to WARNING
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # Set the logging level for asyncio to WARNING
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    app.logger = logging.getLogger(__name__)


    return app



