# Desc: Merchant model for receipt processing
from database import db
from .. import BaseModel

class Merchant(BaseModel):
    """
    Description: This class represents the merchants table for normalizing store/business data.
    Attributes:
        name (str): The normalized name of the merchant.
        address (str): The merchant's address.
        phone (str): The merchant's phone number.
        category_id (int): Reference to the merchant's primary category.
    """
    __tablename__ = 'merchants'

    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Relationships
    receipts = db.relationship('Receipt', backref='merchant', lazy=True)

    def serialize(self):
        base_data = super().serialize()  # Get base fields
        base_data.update({
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        })
        return base_data