# WashLogs System Architecture

This document covers the technology choices, project directories, and database schemas for the WashLogs system.

## 🛠️ Tech Stack
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy
- **Auth**: Supabase Authentication
- **Validation**: Pydantic V2
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

## 📁 System Architecture / Project Structure
```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Configuration & environment
│   │   └── database.py         # Database initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models (API validation)
│   │   └── database.py         # SQLAlchemy models (DB schema)
│   ├── services/
│   │   ├── __init__.py
│   │   └── order_service.py    # Business logic
│   ├── routes/
│   │   ├── __init__.py
│   │   └── order_controller.py # API endpoints/routes
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py    # Error handling & logging
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Utility functions
├── tests/
│   └── test_api.py             # API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 💾 Database Schema

### Orders Table
```sql
CREATE TABLE orders (
  id VARCHAR(36) PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'RECEIVED',
  total_amount FLOAT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NULL,
  INDEX idx_status (status),
  INDEX idx_customer_name (customer_name),
  INDEX idx_phone_number (phone_number)
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
  id VARCHAR(36) PRIMARY KEY,
  order_id VARCHAR(36) NOT NULL FOREIGN KEY,
  garment_type VARCHAR(50) NOT NULL,
  quantity INTEGER NOT NULL,
  price_per_item FLOAT NOT NULL,
  INDEX idx_order_id (order_id)
);
```
