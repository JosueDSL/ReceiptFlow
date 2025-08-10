# models/category.py
from database import db
from .. import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    color = db.Column(db.String(7), default='#6B7280')
    budget_limit = db.Column(db.Numeric(10, 2), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # other relationships (non-self-referential) can stay here
    receipts = db.relationship('Receipt', backref='category', lazy=True)
    receipt_items = db.relationship('ReceiptItem', backref='category', lazy=True)

    def serialize(self):
        base_data = super().serialize()
        base_data.update({
            'name': self.name,
            'parent_id': self.parent_id,
            'parent_name': self.parent.name if getattr(self, 'parent', None) else None,
            'color': self.color,
            'budget_limit': float(self.budget_limit) if self.budget_limit else None,
            'is_active': self.is_active,
            'subcategories_count': len(self.subcategories) if getattr(self, 'subcategories', None) else 0
        })
        return base_data


# define the self-referential relationship *after* the class definition
Category.parent = db.relationship(
    'Category',
    remote_side=[Category.id],          # unambiguous Column expression
    foreign_keys=[Category.parent_id],  # explicitly say which FK is used
    backref=db.backref('subcategories', lazy='select'),
    lazy='joined'
)
