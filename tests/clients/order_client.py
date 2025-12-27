"""Order API client."""
from typing import List, Dict
from requests import Response
from tests.clients.api_client import APIClient


class OrderClient(APIClient):
    """Client for order endpoints."""
    
    def create_order(self, token: str, items: List[Dict[str, any]]) -> Response:
        """Create a new order (customer only)."""
        data = {
            "items": items
        }
        return self.post("/orders", json_data=data, headers=self.auth_headers(token))
    
    def get_order(self, token: str, order_id: str) -> Response:
        """Get an order by ID."""
        return self.get(f"/orders/{order_id}", headers=self.auth_headers(token))
    
    def cancel_order(self, token: str, order_id: str) -> Response:
        """Cancel an order (customer only)."""
        return self.post(f"/orders/{order_id}/cancel", headers=self.auth_headers(token))
