"""
Unit tests for WashLogs backend.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.config.database import get_db
from src.models.database import Base
from src.models.schemas import OrderCreate, OrderItemCreate, GarmentType
from src.middleware.auth import get_current_user
from sqlalchemy.pool import StaticPool

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

def override_get_current_user():
    return {"id": "dummy_user_id"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


class TestHealth:
    """Health check tests."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestOrderCreation:
    """Order creation tests."""

    def test_create_order_success(self):
        """Test successful order creation."""
        payload = {
            "customer_name": "John Doe",
            "phone_number": "9876543210",
            "items": [
                {
                    "garment_type": "Shirt",
                    "quantity": 2,
                    "price_per_item": 50.0
                }
            ]
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["customer_name"] == "John Doe"
        assert data["total_amount"] == 100.0
        assert data["status"] == "RECEIVED"
        assert len(data["items"]) == 1

    def test_create_order_with_multiple_items(self):
        """Test order creation with multiple items."""
        payload = {
            "customer_name": "Jane Smith",
            "phone_number": "8765432109",
            "items": [
                {"garment_type": "Shirt", "quantity": 1, "price_per_item": 50.0},
                {"garment_type": "Pants", "quantity": 2, "price_per_item": 100.0},
                {"garment_type": "Saree", "quantity": 1, "price_per_item": 150.0}
            ]
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total_amount"] == 400.0  # 50 + 200 + 150

    def test_create_order_invalid_phone(self):
        """Test order creation with invalid phone number."""
        payload = {
            "customer_name": "John Doe",
            "phone_number": "123",  # Too short
            "items": [{"garment_type": "Shirt", "quantity": 1, "price_per_item": 50.0}]
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 422

    def test_create_order_empty_items(self):
        """Test order creation with no items."""
        payload = {
            "customer_name": "John Doe",
            "phone_number": "9876543210",
            "items": []
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 422

    def test_create_order_invalid_price(self):
        """Test order creation with invalid price."""
        payload = {
            "customer_name": "John Doe",
            "phone_number": "9876543210",
            "items": [{"garment_type": "Shirt", "quantity": 1, "price_per_item": -50}]
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 422


class TestOrderRetrieval:
    """Order retrieval tests."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data."""
        self.payload = {
            "customer_name": "Test User",
            "phone_number": "9999999999",
            "items": [{"garment_type": "Shirt", "quantity": 1, "price_per_item": 50.0}]
        }
        response = client.post("/api/orders", json=self.payload)
        self.order_id = response.json()["id"]

    def test_get_order_by_id(self):
        """Test retrieving order by ID."""
        response = client.get(f"/api/orders/{self.order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.order_id
        assert data["customer_name"] == "Test User"

    def test_get_nonexistent_order(self):
        """Test retrieving non-existent order."""
        response = client.get("/api/orders/nonexistent-id")
        assert response.status_code == 404

    def test_list_orders(self):
        """Test listing orders."""
        response = client.get("/api/orders")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_list_orders_with_filter(self):
        """Test listing orders with filters."""
        response = client.get(f"/api/orders?customer_name=Test")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1


class TestOrderStatusUpdate:
    """Order status update tests."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data."""
        payload = {
            "customer_name": "Status Test User",
            "phone_number": "8888888888",
            "items": [{"garment_type": "Pants", "quantity": 1, "price_per_item": 100.0}]
        }
        response = client.post("/api/orders", json=payload)
        self.order_id = response.json()["id"]

    def test_update_status_to_processing(self):
        """Test updating order status to PROCESSING."""
        response = client.patch(
            f"/api/orders/{self.order_id}/status",
            json={"status": "PROCESSING"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PROCESSING"

    def test_update_status_to_ready(self):
        """Test updating order status to READY."""
        # First update to PROCESSING
        client.patch(f"/api/orders/{self.order_id}/status", json={"status": "PROCESSING"})
        
        # Then update to READY
        response = client.patch(
            f"/api/orders/{self.order_id}/status",
            json={"status": "READY"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "READY"

    def test_update_status_to_delivered(self):
        """Test updating order status to DELIVERED."""
        response = client.patch(
            f"/api/orders/{self.order_id}/status",
            json={"status": "DELIVERED"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "DELIVERED"

    def test_update_nonexistent_order_status(self):
        """Test updating status of non-existent order."""
        response = client.patch(
            "/api/orders/nonexistent-id/status",
            json={"status": "PROCESSING"}
        )
        assert response.status_code == 404


class TestDashboard:
    """Dashboard endpoint tests."""

    def test_get_dashboard(self):
        """Test getting dashboard statistics."""
        # Create some test orders first
        for i in range(3):
            payload = {
                "customer_name": f"Customer {i}",
                "phone_number": f"999999999{i}",
                "items": [{"garment_type": "Shirt", "quantity": 1, "price_per_item": 50.0}]
            }
            client.post("/api/orders", json=payload)

        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "total_orders" in data
        assert "total_revenue" in data
        assert "orders_by_status" in data
        assert "recent_orders" in data
        assert data["total_orders"] >= 3