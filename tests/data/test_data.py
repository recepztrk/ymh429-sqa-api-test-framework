"""Test data generators and constants."""
import uuid
from typing import List, Dict


# User data
def generate_test_email() -> str:
    """Generate unique test email."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def generate_customer_data() -> Dict[str, str]:
    """Generate customer registration data."""
    return {
        "email": generate_test_email(),
        "password": "password123",
        "role": "customer"
    }


def generate_admin_data() -> Dict[str, str]:
    """Generate admin registration data."""
    return {
        "email": generate_test_email(),
        "password": "admin123",
        "role": "admin"
    }


# Product data
def generate_product_data(name: str = None, price: float = 100.0, stock: int = 10) -> Dict:
    """Generate product creation data."""
    if name is None:
        name = f"Product_{uuid.uuid4().hex[:8]}"
    
    return {
        "name": name,
        "price": price,
        "currency": "TRY",
        "stock": stock,
        "isActive": True
    }


# Order data
def create_order_item(product_id: str, qty: int) -> Dict[str, any]:
    """Create an order item."""
    return {
        "productId": product_id,
        "qty": qty
    }


def create_order_items(product_id: str, qty: int = 1) -> List[Dict]:
    """Create order items list."""
    return [create_order_item(product_id, qty)]


# Payment data
PAYMENT_METHOD_CARD = "CARD"
PAYMENT_METHOD_TRANSFER = "TRANSFER"


# Business rule constants
MIN_CART_TOTAL = 50.0
MAX_CART_TOTAL = 5000.0
MIN_QTY = 1
MAX_QTY = 10
