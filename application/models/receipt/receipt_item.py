# Desc: Receipt item model for line-item tracking
from database import db
from .. import BaseModel

class ReceiptItem(BaseModel):
    """
    Description: This class represents individual line items from receipts.
    Attributes:
        receipt_id (int): Reference to the parent receipt.
        description (str): Description of the item.
        quantity (decimal): Quantity purchased.
        unit_price (decimal): Price per unit.
        total_price (decimal): Total price for this line item.
        category_id (int): Category for this specific item.
    """
    __tablename__ = 'receipt_items'

    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(8, 3), default=1, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    def serialize(self):
        base_data = super().serialize()  # Get base fields
        base_data.update({
            'receipt_id': self.receipt_id,
            'description': self.description,
            'quantity': float(self.quantity),
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        })
        return base_data