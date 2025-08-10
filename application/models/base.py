# Desc: Base model class with common fields and methods
from database import db
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

class BaseModel(db.Model):
    """
    Abstract base model that provides common fields and methods for all models.

    Attributes:
        id (int): Auto-incrementing primary key
        uuid (str): Universal unique identifier for external integrations
        created_at (DateTime): Timestamp when record was created
        updated_at (DateTime): Timestamp when record was last updated
    """
    __abstract__ = True  # This prevents SQLAlchemy from creating a base_model table

    # Common fields for all models
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(PG_UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def save(self):
        """
        Save the current model instance to the database.
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """
        Delete the current model instance from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """
        Update model fields with provided keyword arguments.
        
        Args:
            **kwargs: Field names and values to update
            
        Returns:
            self: The updated model instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    def to_dict(self):
        """
        Convert model instance to dictionary.
        Override this method in child classes for custom serialization.
        
        Returns:
            dict: Dictionary representation of the model
        """
        return {
            'id': self.id,
            'uuid': self.uuid,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def serialize(self):
        """
        Alias for to_dict() to maintain consistency with existing models.

        Returns:
            dict: Dictionary representation of the model
        """
        return self.to_dict()

    @classmethod
    def find_by_uuid(cls, uuid_value):
        """
        Find a model instance by its UUID.
        
        Args:
            uuid_value (str): The UUID to search for
            
        Returns:
            Model instance or None if not found
        """
        return cls.query.filter_by(uuid=uuid_value).first()

    @classmethod
    def find_by_id(cls, id_value):
        """
        Find a model instance by its ID.
        
        Args:
            id_value (int): The ID to search for
            
        Returns:
            Model instance or None if not found
        """
        return cls.query.get(id_value)

    def __repr__(self):
        """
        String representation of the model.
        
        Returns:
            str: String representation showing class name and ID
        """
        return f'<{self.__class__.__name__}(id={self.id}, uuid={self.uuid})>'