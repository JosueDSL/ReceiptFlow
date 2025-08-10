# Description: User model for authentication and user management
from database import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from .. import BaseModel

class User(BaseModel, UserMixin):
    """
    Description: This class represents the user table in the database.
    Inherits common fields (id, uuid, created_at, updated_at) from BaseModel.

    Attributes:
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        last_login (DateTime): The date and time of the user's last login.
    """
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    receipts = db.relationship('Receipt', backref='user', lazy=True, cascade="all, delete-orphan") # Define cascade delete

    # Set the password attribute to be write-only
    @property
    def password(self):
        """
        Prevents reading the password attribute.
        Raises:
            AttributeError: Always raises an AttributeError to prevent reading the password.
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str) -> None:
        """
        Hashes the password and stores it in the password_hash attribute.
        Args:
            password (str): The plaintext password to be hashed.
        """
        self.password_hash = generate_password_hash(password).decode('utf8')

    def verify_password(self, password: str) -> bool:
        """
        Verifies the provided password against the stored password hash.
        Args:
            password (str): The plaintext password to verify.
        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """
        Updates the last_login timestamp to current time.
        """
        from datetime import datetime, timezone
        self.last_login = datetime.now(timezone.utc)
        self.save()

    def serialize(self):
        """
        Override the base serialize method to include user-specific fields.
        Returns:
            dict: Dictionary containing user data (excludes password_hash for security)
        """
        base_data = super().serialize()  # Get base fields (id, uuid, created_at, updated_at)
        base_data.update({
            'username': self.username,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'receipt_count': len(self.receipts) if self.receipts else 0
        })
        return base_data

    @classmethod
    def find_by_username(cls, username: str):
        """
        Find a user by their username.
        Args:
            username (str): The username to search for
        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        """
        String representation of the user.
        Returns:
            str: String representation showing username and ID
        """
        return f'<User(id={self.id}, username={self.username}, uuid={self.uuid})>'