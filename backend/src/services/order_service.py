"""
Service layer containing core business logic for orders.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional
from datetime import datetime
import logging
from src.models.schemas import (
    OrderCreate, OrderResponse, OrderItemResponse, 
    OrderListResponse, DashboardStats, OrderStatus
)
from src.models.database import Order, OrderItem

logger = logging.getLogger(__name__)


class OrderService:
    """Service for managing orders."""

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> OrderResponse:
        """
        Create a new order with items.
        
        Args:
            db: Database session
            order_data: Order creation data
            
        Returns:
            Created order with items
            
        Raises:
            Exception: If order creation fails
        """
        try:
            # Calculate total amount
            total_amount = sum(
                item.quantity * item.price_per_item 
                for item in order_data.items
            )
            total_amount = round(total_amount, 2)

            # Create order
            db_order = Order(
                customer_name=order_data.customer_name,
                phone_number=order_data.phone_number,
                status=OrderStatus.RECEIVED.value,
                total_amount=total_amount
            )
            db.add(db_order)
            db.flush()  # Flush to get the order ID

            # Create order items
            for item in order_data.items:
                db_item = OrderItem(
                    order_id=db_order.id,
                    garment_type=item.garment_type.value,
                    quantity=item.quantity,
                    price_per_item=item.price_per_item
                )
                db.add(db_item)

            db.commit()
            db.refresh(db_order)

            logger.info(f"✓ Order created: {db_order.id} for {order_data.customer_name}")
            return OrderService._map_order_to_response(db_order)

        except Exception as e:
            db.rollback()
            logger.error(f"✗ Failed to create order: {str(e)}")
            raise

    @staticmethod
    def get_order(db: Session, order_id: str) -> Optional[OrderResponse]:
        """
        Retrieve a single order by ID.
        
        Args:
            db: Database session
            order_id: Order ID
            
        Returns:
            Order with items or None
        """
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if db_order:
            return OrderService._map_order_to_response(db_order)
        return None

    @staticmethod
    def get_all_orders(
        db: Session,
        status: Optional[str] = None,
        customer_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[OrderListResponse], int]:
        """
        Retrieve all orders with optional filters.
        
        Args:
            db: Database session
            status: Filter by order status
            customer_name: Filter by customer name (partial match)
            phone_number: Filter by phone number (partial match)
            limit: Limit results
            offset: Offset for pagination
            
        Returns:
            Tuple of (orders, total_count)
        """
        query = db.query(Order)

        # Apply filters
        if status:
            query = query.filter(Order.status == status)
        if customer_name:
            query = query.filter(Order.customer_name.ilike(f"%{customer_name}%"))
        if phone_number:
            query = query.filter(Order.phone_number.ilike(f"%{phone_number}%"))

        # Get total count
        total_count = query.count()

        # Apply pagination and sort by created_at descending
        orders = query.order_by(Order.created_at.desc()).limit(limit).offset(offset).all()

        return [
            OrderListResponse(
                id=o.id,
                customer_name=o.customer_name,
                phone_number=o.phone_number,
                status=OrderStatus[o.status],
                total_amount=o.total_amount,
                created_at=o.created_at
            )
            for o in orders
        ], total_count

    @staticmethod
    def update_order_status(db: Session, order_id: str, new_status: OrderStatus) -> Optional[OrderResponse]:
        """
        Update order status.
        
        Args:
            db: Database session
            order_id: Order ID
            new_status: New status
            
        Returns:
            Updated order or None if not found
        """
        try:
            db_order = db.query(Order).filter(Order.id == order_id).first()
            if not db_order:
                return None

            db_order.status = new_status.value
            db_order.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_order)

            logger.info(f"✓ Order {order_id} status updated to {new_status.value}")
            return OrderService._map_order_to_response(db_order)

        except Exception as e:
            db.rollback()
            logger.error(f"✗ Failed to update order status: {str(e)}")
            raise

    @staticmethod
    def delete_order(db: Session, order_id: str) -> bool:
        """
        Delete an order and its items.
        
        Args:
            db: Database session
            order_id: Order ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            db_order = db.query(Order).filter(Order.id == order_id).first()
            if not db_order:
                return False

            db.delete(db_order)
            db.commit()

            logger.info(f"✓ Order {order_id} deleted")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"✗ Failed to delete order: {str(e)}")
            raise

    @staticmethod
    def get_dashboard_stats(db: Session) -> DashboardStats:
        """
        Get dashboard statistics.
        
        Args:
            db: Database session
            
        Returns:
            Dashboard statistics
        """
        try:
            # Total orders
            total_orders = db.query(func.count(Order.id)).scalar() or 0

            # Total revenue
            total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
            total_revenue = round(float(total_revenue), 2)

            # Orders grouped by status
            status_counts = db.query(
                Order.status,
                func.count(Order.id).label('count')
            ).group_by(Order.status).all()

            orders_by_status = {
                status: count for status, count in status_counts
            }

            # Recent orders (5 most recent)
            recent_orders_db = db.query(Order).order_by(
                Order.created_at.desc()
            ).limit(5).all()

            recent_orders = [
                OrderListResponse(
                    id=o.id,
                    customer_name=o.customer_name,
                    phone_number=o.phone_number,
                    status=OrderStatus[o.status],
                    total_amount=o.total_amount,
                    created_at=o.created_at
                )
                for o in recent_orders_db
            ]

            logger.info("✓ Dashboard stats retrieved")
            return DashboardStats(
                total_orders=total_orders,
                total_revenue=total_revenue,
                orders_by_status=orders_by_status,
                recent_orders=recent_orders
            )

        except Exception as e:
            logger.error(f"✗ Failed to get dashboard stats: {str(e)}")
            raise

    @staticmethod
    def _map_order_to_response(db_order: Order) -> OrderResponse:
        """Convert database order to response model."""
        items = [
            OrderItemResponse(
                id=item.id,
                order_id=item.order_id,
                garment_type=item.garment_type,
                quantity=item.quantity,
                price_per_item=item.price_per_item,
                total_price=item.total_price
            )
            for item in db_order.items
        ]

        return OrderResponse(
            id=db_order.id,
            customer_name=db_order.customer_name,
            phone_number=db_order.phone_number,
            status=OrderStatus[db_order.status],
            total_amount=db_order.total_amount,
            items=items,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at
        )