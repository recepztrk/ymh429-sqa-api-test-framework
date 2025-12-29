"""Test data generators and constants."""
import math 
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
MAX_QTY_PER_ITEM = 10

def pick_valid_product_and_qty(products,
                               min_total: float = MIN_CART_TOTAL,
                               max_total: float = MAX_CART_TOTAL,
                               max_qty: int = MAX_QTY_PER_ITEM):
    """
    Pick a product+qty that satisfies business rules:
    - min_total <= price*qty <= max_total
    - qty <= max_qty
    - stock (if present) >= qty
    Returns: (product_id, qty)
    """
    # 1) Prefer a single-item order where price itself is within bounds
    for p in products:
        price = float(p["price"])
        stock = int(p.get("stock", 10**9))
        if price <= 0:
            continue
        if min_total <= price <= max_total and stock >= 1:
            return p["id"], 1

    # 2) Otherwise choose qty to reach min_total without exceeding max_total
    candidates = []
    for p in products:
        price = float(p["price"])
        stock = int(p.get("stock", 10**9))
        if price <= 0 or price > max_total:
            continue

        qty = int(math.ceil(min_total / price))
        if qty < 1:
            qty = 1

        if qty <= max_qty and (price * qty) <= max_total and stock >= qty:
            candidates.append((p["id"], qty, price * qty))

    if candidates:
        # deterministic: choose the smallest total
        candidates.sort(key=lambda x: x[2])
        return candidates[0][0], candidates[0][1]

    raise AssertionError("No valid product+qty found under cart rules (min/max/qty/stock).")
