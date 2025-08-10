# Description: User service class to handle user related operations.

# Import the required libraries
from datetime import datetime
from flask import make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

# Import the required modules and database
from application.services import BaseValidationService
from application.models import User
from database import db


class UserService(BaseValidationService):
    """
    User service class to handle user related operations.
    """

    def __init__(self, payload):
        super().__init__(payload)


    def register_user(self) -> dict:
        """

        Args:
            None    

        Raises:
            ValueError: If the username or password is missing or does not meet the requirements.
        
        Returns:
            JSON: The response JSON with the user details.
        """

        # Validate the payload
        self.validate_payload()

        # Get the username and password from the payload
        username = self.payload['username']
        password = self.payload['password']

        # Check if the username already exists
        existing_user = self.get_user(username)

        # Raise an error if the username already exists
        if existing_user:
            raise ValueError('Username already exists. Please choose a different username.')

        # Create a new user object
        new_user = User(username=username)
        
        # Set the password for the new user
        new_user.password = password

        # Set the date of registration as the last login time
        new_user.last_login = datetime.utcnow()
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user after registration
        access_token = create_access_token(identity=new_user.id)

        # Set the JSON response
        response = make_response({
            'id': new_user.id,
            'user': new_user.serialize(),
            'message': 'User registered successfully.'
        }, 201)

        # Set the access token in the response
        set_access_cookies(response, access_token)

        return response



