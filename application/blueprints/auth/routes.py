# Import flask and the necessary dependencies
from flask import Blueprint, jsonify, current_app as app
from flask_jwt_extended import jwt_required

from application.blueprints.decorators import handle_request_exceptions
from application.services.auth_service import AuthService
from application.services.request_service import extract_json_payload
from application.services.request_service.request_validator import AuthValidationMixin


# Create a blueprint object
auth_bp = Blueprint('auth', __name__)


# Health check route
@auth_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint for auth service"""
    return jsonify({'status': 'healthy', 'service': 'auth'}), 200


# Login route
@auth_bp.route('/login', methods=['POST'], endpoint='user_login')
@handle_request_exceptions
def login_user_endpoint():
    """
    User login endpoint with comprehensive validation
    
    Expected JSON payload:
    {
        "username": "user@example.com",
        "password": "securepassword"
    }
    """
    # Safely extract JSON payload
    payload = extract_json_payload()
    
    # Validate login request structure
    AuthValidationMixin.validate_login_request(payload)
    
    # Create auth service and process login
    auth_service = AuthService(payload)

    response = auth_service.login_user()

    return response

# Logout route
@auth_bp.route('/logout', methods=['POST'], endpoint='user_logout')
@handle_request_exceptions
@jwt_required()
def logout_user_endpoint():
    # Get the payload from the request
    payload = extract_json_payload()

    # Create a new user service object
    auth_service = AuthService(payload)
    # Logout the user
    response = auth_service.logout_user()

    return response


# Test protected route
@auth_bp.route('/protected', methods=['GET'], endpoint='test')
@handle_request_exceptions
@jwt_required()
def test_endpoint():
    """Protected route for testing authentication"""
    return jsonify({
        'message': 'You are authorized to access this route',
        'success': True
    }), 200