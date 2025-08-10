# Description: Database seeder for ReceiptFlow expense tracking system

from application.models import User, Category, Merchant, Receipt, ReceiptItem, BankTransaction
from flask import current_app as app
from . import db
import random
from datetime import datetime, timedelta
from decimal import Decimal

class StartupSeeder:
    def __init__(self, app):
        self.app = app

    def seed(self):
        with self.app.app_context():
            # Create default user if none exists
            user = self._create_default_user()
            
            # Create default categories
            categories = self._create_categories()
            
            # Create sample merchants
            merchants = self._create_merchants(categories)
            
            # Create sample receipts with items
            receipts = self._create_sample_receipts(merchants, categories)
            
            # Create sample bank transactions
            self._create_bank_transactions(receipts)
            
            app.logger.info('ReceiptFlow database seeded successfully.')

    def _create_default_user(self):
        """Create default user if none exists"""
        user = User.query.first()
        if not user:
            user = User(username='admin')
            user.password = 'admin123'
            db.session.add(user)
            db.session.flush()
            app.logger.info('Default user created.')
        return user

    def _create_categories(self):
        """Create hierarchical expense categories"""
        if Category.query.count() > 0:
            return Category.query.all()

        # Main categories
        main_categories_data = [
            {'name': 'Food & Dining', 'color': '#FF6B6B', 'budget_limit': 500.00},
            {'name': 'Transportation', 'color': '#4ECDC4', 'budget_limit': 300.00},
            {'name': 'Shopping', 'color': '#45B7D1', 'budget_limit': 400.00},
            {'name': 'Entertainment', 'color': '#96CEB4', 'budget_limit': 200.00},
            {'name': 'Bills & Utilities', 'color': '#FFEAA7', 'budget_limit': 800.00},
            {'name': 'Healthcare', 'color': '#DDA0DD', 'budget_limit': 250.00},
            {'name': 'Travel', 'color': '#98D8C8', 'budget_limit': 600.00},
            {'name': 'Personal Care', 'color': '#F7DC6F', 'budget_limit': 150.00},
            {'name': 'Home & Garden', 'color': '#BB8FCE', 'budget_limit': 300.00},
            {'name': 'Education', 'color': '#85C1E9', 'budget_limit': 200.00}
        ]

        main_categories = []
        for cat_data in main_categories_data:
            category = Category(**cat_data)
            main_categories.append(category)
            db.session.add(category)
        
        db.session.flush()  # Get IDs for parent relationships

        # Subcategories
        subcategories_data = [
            # Food & Dining subcategories
            {'name': 'Groceries', 'parent_id': main_categories[0].id, 'color': '#FF8E8E'},
            {'name': 'Restaurants', 'parent_id': main_categories[0].id, 'color': '#FF7979'},
            {'name': 'Fast Food', 'parent_id': main_categories[0].id, 'color': '#FFB3B3'},
            {'name': 'Coffee Shops', 'parent_id': main_categories[0].id, 'color': '#FF9F9F'},
            
            # Transportation subcategories  
            {'name': 'Gas & Fuel', 'parent_id': main_categories[1].id, 'color': '#6BCCC8'},
            {'name': 'Public Transit', 'parent_id': main_categories[1].id, 'color': '#54E0D6'},
            {'name': 'Parking', 'parent_id': main_categories[1].id, 'color': '#7FDDDA'},
            {'name': 'Car Maintenance', 'parent_id': main_categories[1].id, 'color': '#42C4C1'},
            
            # Shopping subcategories
            {'name': 'Clothing', 'parent_id': main_categories[2].id, 'color': '#65C3E3'},
            {'name': 'Electronics', 'parent_id': main_categories[2].id, 'color': '#5AB9DA'},
            {'name': 'Books & Media', 'parent_id': main_categories[2].id, 'color': '#6FD0E7'},
            {'name': 'Gifts', 'parent_id': main_categories[2].id, 'color': '#7AD6EA'},
            
            # Entertainment subcategories
            {'name': 'Movies & Shows', 'parent_id': main_categories[3].id, 'color': '#A8D5C4'},
            {'name': 'Sports & Recreation', 'parent_id': main_categories[3].id, 'color': '#B2DAC9'},
            {'name': 'Hobbies', 'parent_id': main_categories[3].id, 'color': '#9CD1C0'},
            
            # Bills & Utilities subcategories
            {'name': 'Electricity', 'parent_id': main_categories[4].id, 'color': '#FFF2C7'},
            {'name': 'Internet & Phone', 'parent_id': main_categories[4].id, 'color': '#FFF5D1'},
            {'name': 'Insurance', 'parent_id': main_categories[4].id, 'color': '#FFEFB8'},
        ]

        subcategories = []
        for subcat_data in subcategories_data:
            subcategory = Category(**subcat_data)
            subcategories.append(subcategory)
            db.session.add(subcategory)

        db.session.commit()
        app.logger.info(f'Created {len(main_categories)} main categories and {len(subcategories)} subcategories.')
        
        return main_categories + subcategories

    def _create_merchants(self, categories):
        """Create sample merchants"""
        if Merchant.query.count() > 0:
            return Merchant.query.all()

        # Find category IDs for merchant assignment
        grocery_cat = Category.query.filter_by(name='Groceries').first()
        restaurant_cat = Category.query.filter_by(name='Restaurants').first()
        gas_cat = Category.query.filter_by(name='Gas & Fuel').first()
        electronics_cat = Category.query.filter_by(name='Electronics').first()
        coffee_cat = Category.query.filter_by(name='Coffee Shops').first()

        merchants_data = [
            {'name': 'Whole Foods Market', 'address': '123 Organic St, Health City', 'phone': '555-0101', 'category_id': grocery_cat.id if grocery_cat else None},
            {'name': 'Trader Joe\'s', 'address': '456 Fresh Ave, Green Valley', 'phone': '555-0102', 'category_id': grocery_cat.id if grocery_cat else None},
            {'name': 'Safeway', 'address': '789 Main St, Downtown', 'phone': '555-0103', 'category_id': grocery_cat.id if grocery_cat else None},
            {'name': 'Target', 'address': '321 Shopping Blvd, Mall District', 'phone': '555-0104', 'category_id': electronics_cat.id if electronics_cat else None},
            {'name': 'Starbucks', 'address': '654 Coffee Corner, Bean Town', 'phone': '555-0105', 'category_id': coffee_cat.id if coffee_cat else None},
            {'name': 'Shell Gas Station', 'address': '987 Highway 1, Fuel Junction', 'phone': '555-0106', 'category_id': gas_cat.id if gas_cat else None},
            {'name': 'McDonald\'s', 'address': '147 Fast Food Ln, Quick Eats', 'phone': '555-0107', 'category_id': restaurant_cat.id if restaurant_cat else None},
            {'name': 'Olive Garden', 'address': '258 Italian Way, Pasta Plaza', 'phone': '555-0108', 'category_id': restaurant_cat.id if restaurant_cat else None},
            {'name': 'Best Buy', 'address': '369 Tech Street, Electronics Hub', 'phone': '555-0109', 'category_id': electronics_cat.id if electronics_cat else None},
            {'name': 'Home Depot', 'address': '741 Builder Ave, Tool Town', 'phone': '555-0110', 'category_id': None},
        ]

        merchants = []
        for merchant_data in merchants_data:
            merchant = Merchant(**merchant_data)
            merchants.append(merchant)
            db.session.add(merchant)

        db.session.commit()
        app.logger.info(f'Created {len(merchants)} merchants.')
        
        return merchants

    def _create_sample_receipts(self, merchants, categories):
        """Create sample receipts with line items"""
        if Receipt.query.count() > 0:
            return Receipt.query.all()

        # Get the default user
        user = User.query.first()
        if not user:
            raise Exception("No user found. User must be created before receipts.")

        receipts = []
        
        # Generate receipts for the last 30 days
        for i in range(50):  # Create 50 sample receipts
            receipt_date = datetime.now() - timedelta(days=random.randint(0, 30))
            merchant = random.choice(merchants)
            category = random.choice([cat for cat in categories if not cat.parent_id])  # Main categories only
            
            # Generate receipt amounts based on merchant type
            if 'Starbucks' in merchant.name or 'McDonald' in merchant.name:
                base_amount = random.uniform(5.50, 15.99)
            elif 'Gas' in merchant.name or 'Shell' in merchant.name:
                base_amount = random.uniform(25.00, 85.00)
            elif 'Whole Foods' in merchant.name or 'Trader' in merchant.name:
                base_amount = random.uniform(35.00, 120.00)
            else:
                base_amount = random.uniform(15.00, 250.00)
            
            tax_rate = 0.0875  # 8.75% tax
            tax_amount = round(base_amount * tax_rate, 2)
            total_amount = round(base_amount + tax_amount, 2)
            
            # Add tip for restaurants
            tip_amount = None
            if 'Restaurant' in (category.name if category else '') or any(word in merchant.name.lower() for word in ['restaurant', 'olive', 'mcdonald']):
                tip_amount = round(base_amount * random.uniform(0.15, 0.22), 2)
                total_amount += tip_amount

            receipt = Receipt(
                user_id=user.id,  # Add user_id reference
                merchant_id=merchant.id,
                date=receipt_date,
                total_amount=Decimal(str(total_amount)),
                tax_amount=Decimal(str(tax_amount)),
                tip_amount=Decimal(str(tip_amount)) if tip_amount else None,
                image_path=f'/uploads/receipts/receipt_{i+1}_{receipt_date.strftime("%Y%m%d")}.jpg',
                image_hash=f'hash_{i+1}_{random.randint(1000, 9999)}',
                raw_ocr_text=self._generate_sample_ocr_text(merchant.name, total_amount, receipt_date),
                ocr_confidence=random.uniform(0.85, 0.98),
                processing_status=random.choice(['completed', 'completed', 'completed', 'pending', 'needs_review']),
                needs_review=random.choice([False, False, False, False, True]),
                category_id=category.id if category else None
            )
            
            receipts.append(receipt)
            db.session.add(receipt)

        db.session.flush()  # Get receipt IDs

        # Create receipt items for each receipt
        total_items = 0
        for receipt in receipts:
            num_items = random.randint(1, 6)
            items_total = 0
            
            for j in range(num_items):
                # Generate item based on merchant
                item_desc, unit_price = self._generate_item_for_merchant(receipt.merchant.name)
                quantity = random.randint(1, 3)
                total_price = round(unit_price * quantity, 2)
                items_total += total_price
                
                # Find appropriate subcategory
                subcategory = self._get_subcategory_for_item(item_desc, categories)
                
                receipt_item = ReceiptItem(
                    receipt_id=receipt.id,
                    description=item_desc,
                    quantity=Decimal(str(quantity)),
                    unit_price=Decimal(str(unit_price)),
                    total_price=Decimal(str(total_price)),
                    category_id=subcategory.id if subcategory else None
                )
                
                db.session.add(receipt_item)
                total_items += 1

        db.session.commit()
        app.logger.info(f'Created {len(receipts)} receipts with {total_items} total items.')
        
        return receipts

    def _generate_sample_ocr_text(self, merchant_name, total_amount, date):
        """Generate realistic OCR text for receipts"""
        return f"""
{merchant_name}
{date.strftime('%m/%d/%Y %I:%M %p')}

Thank you for shopping with us!
Subtotal: ${total_amount - (total_amount * 0.0875):.2f}
Tax: ${total_amount * 0.0875:.2f}
Total: ${total_amount:.2f}

Card ending in 1234
Transaction ID: TXN{random.randint(100000, 999999)}
""".strip()

    def _generate_item_for_merchant(self, merchant_name):
        """Generate realistic items based on merchant type"""
        if 'Whole Foods' in merchant_name or 'Trader' in merchant_name or 'Safeway' in merchant_name:
            items = [
                ('Organic Bananas', 2.99), ('Greek Yogurt', 4.49), ('Sourdough Bread', 3.99),
                ('Avocados', 1.99), ('Chicken Breast', 8.99), ('Mixed Greens', 3.49),
                ('Almond Milk', 3.99), ('Free-Range Eggs', 4.99), ('Quinoa', 5.99)
            ]
        elif 'Starbucks' in merchant_name:
            items = [
                ('Grande Latte', 4.95), ('Venti Pike Place', 2.45), ('Blueberry Muffin', 2.95),
                ('Caramel Macchiato', 5.45), ('Croissant', 2.75), ('Cold Brew', 3.25)
            ]
        elif 'McDonald' in merchant_name:
            items = [
                ('Big Mac Meal', 9.99), ('McChicken', 4.99), ('Large Fries', 2.99),
                ('McFlurry', 3.49), ('Quarter Pounder', 5.99), ('Apple Pie', 1.99)
            ]
        elif 'Target' in merchant_name or 'Best Buy' in merchant_name:
            items = [
                ('USB Cable', 12.99), ('Phone Case', 24.99), ('Bluetooth Headphones', 79.99),
                ('Notebook', 3.99), ('Pen Set', 8.99), ('Phone Charger', 19.99)
            ]
        else:
            items = [
                ('Miscellaneous Item', 15.99), ('Product', 8.99), ('Service', 25.00),
                ('Supplies', 12.50), ('Equipment', 45.99)
            ]
        
        return random.choice(items)

    def _get_subcategory_for_item(self, item_desc, categories):
        """Find appropriate subcategory for an item"""
        item_lower = item_desc.lower()
        
        # Mapping keywords to subcategory names
        category_mapping = {
            'coffee': 'Coffee Shops',
            'latte': 'Coffee Shops',
            'macchiato': 'Coffee Shops',
            'banana': 'Groceries',
            'yogurt': 'Groceries',
            'bread': 'Groceries',
            'avocado': 'Groceries',
            'chicken': 'Groceries',
            'greens': 'Groceries',
            'milk': 'Groceries',
            'eggs': 'Groceries',
            'quinoa': 'Groceries',
            'mac': 'Fast Food',
            'fries': 'Fast Food',
            'mcchicken': 'Fast Food',
            'burger': 'Fast Food',
            'usb': 'Electronics',
            'phone': 'Electronics',
            'bluetooth': 'Electronics',
            'headphones': 'Electronics',
            'charger': 'Electronics',
            'notebook': 'Books & Media',
            'pen': 'Books & Media'
        }
        
        for keyword, category_name in category_mapping.items():
            if keyword in item_lower:
                return next((cat for cat in categories if cat.name == category_name), None)
        
        return None

    def _create_bank_transactions(self, receipts):
        """Create sample bank transactions for reconciliation"""
        if BankTransaction.query.count() > 0:
            return

        # Create bank transactions for about 70% of receipts
        sample_receipts = random.sample(receipts, int(len(receipts) * 0.7))
        
        transactions = []
        for receipt in sample_receipts:
            # Sometimes the bank amount differs slightly from receipt total
            amount_variance = random.uniform(-0.50, 0.50) if random.random() < 0.1 else 0
            bank_amount = float(receipt.total_amount) + amount_variance
            
            transaction = BankTransaction(
                date=receipt.date,
                amount=Decimal(str(round(bank_amount, 2))),
                merchant_name=receipt.merchant.name,
                account_id=f"ACCT{random.randint(1000, 9999)}",
                receipt_id=receipt.id
            )
            
            transactions.append(transaction)
            db.session.add(transaction)

        # Add some unmatched bank transactions
        for i in range(10):
            transaction_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            transaction = BankTransaction(
                date=transaction_date,
                amount=Decimal(str(round(random.uniform(10.00, 150.00), 2))),
                merchant_name=f"Unknown Merchant {i+1}",
                account_id=f"ACCT{random.randint(1000, 9999)}",
                receipt_id=None  # Unmatched
            )
            
            transactions.append(transaction)
            db.session.add(transaction)

        db.session.commit()
        app.logger.info(f'Created {len(transactions)} bank transactions.')