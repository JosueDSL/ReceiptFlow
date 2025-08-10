# ReceiptFlow
Expense tracking system that automatically processes receipt images using OCR technology, categorizes expenses intelligently, and provides comprehensive spending analytics.

## Project Structure
```bash
ReceiptFlow/
├── app/
│   ├── __init__.py              # Flask app factory with extensions
│   ├── config.py                # Environment-based configuration
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── receipt.py           # Receipt & ReceiptItem models
│   │   ├── merchant.py          # Merchant normalization
│   │   ├── category.py          # Hierarchical categories
│   │   └── transaction.py       # Bank transaction matching
│   ├── api/                     # RESTful API blueprints
│   │   ├── receipts.py          # Upload, CRUD, status endpoints
│   │   ├── analytics.py         # Spending reports & insights
│   │   ├── merchants.py         # Merchant management
│   │   └── categories.py        # Category management
│   ├── services/                # Business logic layer
│   │   ├── ocr_service.py       # Multi-engine OCR processing
│   │   ├── parser_service.py    # Receipt text parsing logic
│   │   ├── categorizer.py       # ML-based auto-categorization
│   │   └── notification_service.py # Alert system
│   ├── utils/                   # Shared utilities
│   │   ├── image_processing.py  # OpenCV preprocessing
│   │   ├── validators.py        # Input validation & security
│   │   └── helpers.py           # Common utility functions
│   └── tasks/                   # Background processing
│       └── background_tasks.py  # Celery task definitions
├── migrations/                  # Flask-Migrate database versions
├── uploads/                     # Receipt image storage
├── tests/                       # Comprehensive test suite
├── docker-compose.yml           # Multi-container orchestration
└── requirements.txt             # Python dependencies
```