"""In-memory storage for users, products, orders, and payments."""
import threading
from typing import Dict, Optional, List
from api.models import UserInternal, Product, Order, Payment


class InMemoryStorage:
    """Thread-safe in-memory storage."""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.users: Dict[str, UserInternal] = {}  # keyed by email
        self.products: Dict[str, Product] = {}  # keyed by id
        self.orders: Dict[str, Order] = {}  # keyed by id
        self.payments: Dict[str, Payment] = {}  # keyed by id
        self.payment_by_order: Dict[str, str] = {}  # order_id -> payment_id
    
    # ========== Users ==========
    def add_user(self, user: UserInternal) -> UserInternal:
        with self._lock:
            self.users[user.email] = user
            return user
    
    def get_user_by_email(self, email: str) -> Optional[UserInternal]:
        with self._lock:
            return self.users.get(email)
    
    def get_user_by_id(self, user_id: str) -> Optional[UserInternal]:
        with self._lock:
            for user in self.users.values():
                if user.id == user_id:
                    return user
            return None
    
    # ========== Products ==========
    def add_product(self, product: Product) -> Product:
        with self._lock:
            self.products[product.id] = product
            return product
    
    def get_product(self, product_id: str) -> Optional[Product]:
        with self._lock:
            return self.products.get(product_id)
    
    def update_product(self, product_id: str, product: Product) -> Optional[Product]:
        with self._lock:
            if product_id in self.products:
                self.products[product_id] = product
                return product
            return None
    
    def list_products(self, active_only: bool = True) -> List[Product]:
        with self._lock:
            if active_only:
                return [p for p in self.products.values() if p.isActive]
            return list(self.products.values())
    
    def decrease_stock(self, product_id: str, qty: int) -> bool:
        """Decrease product stock. Returns True if successful, False if insufficient stock."""
        with self._lock:
            product = self.products.get(product_id)
            if not product or product.stock < qty:
                return False
            product.stock -= qty
            return True
    
    def increase_stock(self, product_id: str, qty: int):
        """Increase product stock (e.g., when order is cancelled)."""
        with self._lock:
            product = self.products.get(product_id)
            if product:
                product.stock += qty
    
    # ========== Orders ==========
    def add_order(self, order: Order) -> Order:
        with self._lock:
            self.orders[order.id] = order
            return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        with self._lock:
            return self.orders.get(order_id)
    
    def update_order(self, order_id: str, order: Order) -> Optional[Order]:
        with self._lock:
            if order_id in self.orders:
                self.orders[order_id] = order
                return order
            return None
    
    # ========== Payments ==========
    def add_payment(self, payment: Payment) -> Payment:
        with self._lock:
            self.payments[payment.id] = payment
            self.payment_by_order[payment.orderId] = payment.id
            return payment
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        with self._lock:
            return self.payments.get(payment_id)
    
    def get_payment_by_order(self, order_id: str) -> Optional[Payment]:
        """Get payment for a specific order."""
        with self._lock:
            payment_id = self.payment_by_order.get(order_id)
            if payment_id:
                return self.payments.get(payment_id)
            return None


# Global storage instance
storage = InMemoryStorage()
