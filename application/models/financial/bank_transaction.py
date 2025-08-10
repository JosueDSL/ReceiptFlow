# Desc: Bank transaction model for reconciliation
from database import db
from .. import BaseModel

class BankTransaction(BaseModel):
    """
    Description: This class represents bank transactions for receipt reconciliation.
    Attributes:
        date (DateTime): The transaction date from the bank.
        amount (decimal): The transaction amount.
        merchant_name (str): Merchant name from bank data.
        account_id (str): Bank account identifier.
        receipt_id (int): Reference to matched receipt.
    """
    __tablename__ = 'bank_transactions'

    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    merchant_name = db.Column(db.String(255), nullable=True)
    account_id = db.Column(db.String(100), nullable=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'), nullable=True)

    # Relationships
    receipt = db.relationship('Receipt', backref='bank_transactions')
    
    def serialize(self):
        base_data = super().serialize()  # Get base fields
        base_data.update({
            'date': self.date.isoformat() if self.date else None,
            'amount': float(self.amount),
            'merchant_name': self.merchant_name,
            'account_id': self.account_id,
            'receipt_id': self.receipt_id,
        })
        return base_data