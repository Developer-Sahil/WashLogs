# WashLogs System Architecture

This document covers the technology choices, project directories, and database schemas for the WashLogs system.

### Backend
- **Framework**: FastAPI 0.136.0
- **Language**: Python 3.12+
- **Database**: PostgreSQL (Supabase) + SQLite (Dev/Test)
- **ORM**: SQLAlchemy 2.0
- **Auth**: Supabase JWT

### Frontend
- **Library**: React 18
- **Build Tool**: Vite
- **Styling**: Vanilla CSS (Skeuomorphic Design System)
- **Networking**: Axios + Vite Proxy
- **State Management**: React Context API (Auth)


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
