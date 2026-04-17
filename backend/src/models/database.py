"""
SQLAlchemy database models for WashLogs.
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Order(Base):
    """Order table model."""
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_name = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="RECEIVED", index=True)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, customer={self.customer_name}, status={self.status})>"


class OrderItem(Base):
    """Order items table model."""
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    garment_type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")

    @property
    def total_price(self):
        """Calculate total price for this item."""
        return round(self.quantity * self.price_per_item, 2)

    def __repr__(self):
        return f"<OrderItem(id={self.id}, garment={self.garment_type}, qty={self.quantity})>"