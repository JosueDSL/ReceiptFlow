# models/receipt/receipt.py
from database import db
from .. import BaseModel

class Receipt(BaseModel):
    """
    Description: This class represents the receipts table for expense tracking.
    Attributes:
        merchant_id (int): Reference to the merchant.
        date (DateTime): The transaction date from the receipt.
        total_amount (decimal): The total amount of the transaction.
        tax_amount (decimal): The tax amount from the receipt.
        tip_amount (decimal): The tip amount if applicable.
        image_path (str): Path to the stored receipt image.
        image_hash (str): SHA256 hash for duplicate detection.
        raw_ocr_text (text): Raw text extracted from OCR.
        ocr_confidence (float): OCR confidence score (0.0 to 1.0).
        processing_status (str): Current processing status.
        needs_review (bool): Flag indicating manual review needed.
        category_id (int): Primary category for this receipt.
    """
    __tablename__ = 'receipts'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=True)
    tip_amount = db.Column(db.Numeric(10, 2), nullable=True)
    image_path = db.Column(db.String(500), nullable=False)
    image_hash = db.Column(db.String(64), unique=True, nullable=False)
    raw_ocr_text = db.Column(db.Text, nullable=True)
    ocr_confidence = db.Column(db.Float, nullable=True)
    processing_status = db.Column(db.String(20), default='pending')
    needs_review = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Relationships
    items = db.relationship('ReceiptItem', backref='receipt', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        base_data = super().serialize()  # Get base fields
        base_data.update({
            'user_id': self.user_id,
            'merchant_id': self.merchant_id,
            'date': self.date.isoformat() if self.date else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'tip_amount': float(self.tip_amount) if self.tip_amount else None,
            'processing_status': self.processing_status,
            'needs_review': self.needs_review,
            'category_id': self.category_id,
            'items_count': len(self.items) if self.items else 0
        })
        return base_data