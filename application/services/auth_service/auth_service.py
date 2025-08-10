# Description: Auth service class to handle authorization related operations.

# Import the required modules and libraries

# Import the required modules and database
from database import db
from application.services import BaseValidationService
from datetime import datetime
from flask import make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies


class AuthService(BaseValidationService):
    """
    Auth service class to handle authentication related operations.
    """

    def __init__(self, payload):
        super().__init__(payload)


    def login_user(self):
        """
        Authenticates a user and generates a JWT token.

        Raises:
            ValueError: If the username or password is incorrect.

        Returns:
            JSON: The response JSON with the JWT token.
        """
        # Validate the payload
        self.validate_payload()

        # Get the username and password from the payload
        username = self.payload['username']
        password = self.payload['password']

        # Find the user by username
        user = self.get_user(username)
        if not user:
            raise ValueError('Invalid username, it does not exists.')
        
        # Verify the password
        if not user.verify_password(password):
            raise ValueError('Invalid password.')

        # Update the last login time
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create a JWT token
        access_token = create_access_token(identity=user.id)

        # Set the JSON response
        response = make_response({
            'user_id': user.id,
            'username': user.username,
            'message': 'User logged in successfully.'
        }, 201)

        # Set the access token in the response
        set_access_cookies(response, access_token)

        return response


    def logout_user(self):
        """
        Logs out the user by clearing the JWT token.

        Returns:
            JSON: The response JSON with the message.
        """
        # Set the JSON response
        response = make_response({
            'message': 'User logged out successfully.'
        }, 200)

        # Clear the JWT cookies in the response
        unset_jwt_cookies(response)

        return response
