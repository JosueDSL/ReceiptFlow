# Description: Base service class to handle shared operations like payload validation.

# Import the User model and the database object
from application.models import User


class BaseValidationService:
    """
    Base service class to handle shared operations like payload validation.
    """

    def __init__(self, payload):
        self.payload = payload


    def get_user(self, username: str) -> User:
        """
        Get the user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user object.
            None: If the user is not found.
        """
        return User.query.filter_by(username=username).first()


    def validate_payload(self) -> None:
        """ Validate the payload for the user service. 
        
        Args:
            None

        Raises:
            ValueError: If the username or password is missing or does not meet the requirements.
        """
        username = self.payload.get('username')
        password = self.payload.get('password')

        # Check if the username and password are provided and meet the requirements
        if not username or not password:
            raise ValueError('Username and password are required.')
        elif len(username) < 4 or len(username) > 50:
            raise ValueError('Username must be between 4 and 50 characters long.')
        elif len(password) < 6 or len(password) > 50:
            raise ValueError('Password must be between 8 and 50 characters long.')

        # Safely convert username and password to strings
        self.payload['username'] = str(username)
        self.payload['password'] = str(password)