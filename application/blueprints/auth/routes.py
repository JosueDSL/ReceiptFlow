# Description: Routes for the auth blueprint.

# Import flask and the necessary dependencies
from flask import Blueprint, request, jsonify, current_app as app
from application.blueprints.helper_methods import ErrorHandler
from application.services import AuthService
from flask_jwt_extended import jwt_required


# Create a blueprint object
auth_bp = Blueprint('auth', __name__)


# Health check route
@auth_bp.route('/health', methods=['GET'])
def health():
    return 'OK', 200



# Login route
@auth_bp.route('/login', methods=['POST'], endpoint='user_login')
@ErrorHandler.handle_exceptions
def login_user_endpoint():
    # Get the payload from the request
    payload = ErrorHandler.get_json_payload()

    # Create a new user service object
    auth_service = AuthService(payload)

    # Login the user
    response = auth_service.login_user()

    return response

# Logout route
@auth_bp.route('/logout', methods=['POST'], endpoint='user_logout')
@ErrorHandler.handle_exceptions
@jwt_required()
def logout_user_endpoint():
    # Get the payload from the request
    payload = ErrorHandler.get_json_payload()

    # Create a new user service object
    auth_service = AuthService(payload)

    # Logout the user
    response = auth_service.logout_user()

    return response



# Test protected route
@auth_bp.route('/protected', methods=['GET'], endpoint='test')
@ErrorHandler.handle_exceptions
@jwt_required()
def test_endpoint():
    return 'You are authorized to access this route', 200