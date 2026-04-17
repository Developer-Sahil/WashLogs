"""
API routes and endpoint handlers for orders.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from src.middleware.auth import get_current_user
from src.config.database import get_db
from src.models.schemas import (
    OrderCreate, OrderResponse, OrderListResponse, 
    DashboardStats, OrderUpdate, OrderStatus, ErrorResponse
)
from src.services.order_service import OrderService

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/orders", 
    tags=["orders"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    responses={
        201: {"description": "Order created successfully"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new laundry order.
    
    **Request body:**
    - `customer_name`: Customer name (required)
    - `phone_number`: Customer phone number (required, min 10 digits)
    - `items`: List of garments with quantity and price
    
    **Returns:**
    - Order ID (UUID)
    - Total bill amount
    - Order status (RECEIVED)
    - Unique order ID
    """
    try:
        order = OrderService.create_order(db, order_data)
        logger.info(f"Order created: {order.id}")
        return order
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get order by ID",
    responses={
        200: {"description": "Order found"},
        404: {"model": ErrorResponse, "description": "Order not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific order by its ID.
    
    **Path parameters:**
    - `order_id`: UUID of the order
    
    **Returns:**
    - Complete order details with all items
    """
    order = OrderService.get_order(db, order_id)
    if not order:
        logger.warning(f"Order not found: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    return order


@router.get(
    "",
    response_model=dict,
    summary="List all orders",
    responses={
        200: {"description": "List of orders"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def list_orders(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    customer_name: Optional[str] = Query(None, description="Filter by customer name"),
    phone_number: Optional[str] = Query(None, description="Filter by phone number"),
    limit: int = Query(100, ge=1, le=500, description="Number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    List all orders with optional filters.
    
    **Query parameters:**
    - `status`: Filter by order status (RECEIVED, PROCESSING, READY, DELIVERED)
    - `customer_name`: Filter by customer name (partial match)
    - `phone_number`: Filter by phone number (partial match)
    - `limit`: Number of results (default: 100)
    - `offset`: Pagination offset (default: 0)
    
    **Returns:**
    - List of orders matching filters
    - Total count of matching orders
    """
    try:
        orders, total = OrderService.get_all_orders(
            db,
            status=status_filter,
            customer_name=customer_name,
            phone_number=phone_number,
            limit=limit,
            offset=offset
        )
        return {
            "data": orders,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list orders"
        )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    summary="Update order status",
    responses={
        200: {"description": "Order updated"},
        404: {"model": ErrorResponse, "description": "Order not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def update_order_status(
    order_id: str,
    status_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of an order.
    
    **Path parameters:**
    - `order_id`: UUID of the order
    
    **Request body:**
    - `status`: New status (RECEIVED, PROCESSING, READY, DELIVERED)
    
    **Returns:**
    - Updated order details
    """
    try:
        order = OrderService.update_order_status(db, order_id, status_update.status)
        if not order:
            logger.warning(f"Order not found for status update: {order_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an order",
    responses={
        204: {"description": "Order deleted"},
        404: {"model": ErrorResponse, "description": "Order not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def delete_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an order and all its items.
    
    **Path parameters:**
    - `order_id`: UUID of the order
    """
    try:
        deleted = OrderService.delete_order(db, order_id)
        if not deleted:
            logger.warning(f"Order not found for deletion: {order_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete order"
        )


# Dashboard Routes
dashboard_router = APIRouter(
    prefix="/api/dashboard", 
    tags=["dashboard"],
    dependencies=[Depends(get_current_user)]
)


@dashboard_router.get(
    "",
    response_model=DashboardStats,
    summary="Get dashboard statistics",
    responses={
        200: {"description": "Dashboard stats"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def get_dashboard(db: Session = Depends(get_db)):
    """
    Get dashboard statistics.
    
    **Returns:**
    - Total number of orders
    - Total revenue from all orders
    - Orders grouped by status
    - 5 most recent orders
    """
    try:
        stats = OrderService.get_dashboard_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard stats"
        )