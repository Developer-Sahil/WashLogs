"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import re


class OrderStatus(str, Enum):
    """Order status enumeration."""
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    DELIVERED = "DELIVERED"


class GarmentType(str, Enum):
    """Garment type enumeration."""
    SHIRT = "Shirt"
    PANTS = "Pants"
    SAREE = "Saree"
    DRESS = "Dress"
    SKIRT = "Skirt"
    JACKET = "Jacket"
    COAT = "Coat"
    SWEATER = "Sweater"
    BLOUSE = "Blouse"
    OTHER = "Other"


class OrderItemCreate(BaseModel):
    """Request model for creating order items."""
    garment_type: GarmentType
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    price_per_item: float = Field(..., gt=0, description="Price must be greater than 0")

    @validator('quantity')
    def validate_quantity(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('Quantity must be a positive integer')
        return v

    @validator('price_per_item')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return round(v, 2)


class OrderItemResponse(OrderItemCreate):
    """Response model for order items."""
    id: str = Field(..., description="Item ID")
    order_id: str = Field(..., description="Order ID")
    total_price: float = Field(..., description="Total price for this item (quantity * price_per_item)")

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Request model for creating orders."""
    customer_name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    phone_number: str = Field(..., description="Phone number")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Order items")

    @validator('phone_number')
    def validate_phone(cls, v):
        # Basic phone validation: at least 10 digits
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v

    @validator('customer_name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Customer name cannot be empty')
        return v.strip()


class OrderUpdate(BaseModel):
    """Request model for updating order status."""
    status: OrderStatus = Field(..., description="New order status")


class OrderResponse(BaseModel):
    """Response model for orders."""
    id: str = Field(..., description="Order ID (UUID)")
    customer_name: str
    phone_number: str
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Response model for orders list."""
    id: str
    customer_name: str
    phone_number: str
    status: OrderStatus
    total_amount: float
    created_at: datetime


class DashboardStats(BaseModel):
    """Dashboard statistics model."""
    total_orders: int = Field(..., description="Total number of orders")
    total_revenue: float = Field(..., description="Total revenue from all orders")
    orders_by_status: dict = Field(..., description="Orders grouped by status")
    recent_orders: List[OrderListResponse] = Field(default_factory=list, description="5 most recent orders")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    details: Optional[str] = None
    status_code: int