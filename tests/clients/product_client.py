"""Product API client."""
from typing import Optional, Dict
from requests import Response
from tests.clients.api_client import APIClient


class ProductClient(APIClient):
    """Client for product endpoints."""
    
    def list_products(self) -> Response:
        """List all active products (no auth required)."""
        return self.get("/products")
    
    def get_product(self, product_id: str) -> Response:
        """Get a specific product by ID (no auth required)."""
        return self.get(f"/products/{product_id}")
    
    def create_product(self, token: str, name: str, price: float, 
                      stock: int, currency: str = "TRY", is_active: bool = True) -> Response:
        """Create a new product (admin only)."""
        data = {
            "name": name,
            "price": price,
            "currency": currency,
            "stock": stock,
            "isActive": is_active
        }
        return self.post("/products", json_data=data, headers=self.auth_headers(token))
    