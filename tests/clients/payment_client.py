"""Payment API client."""
from typing import Optional
from requests import Response
from tests.clients.api_client import APIClient


class PaymentClient(APIClient):
    """Client for payment endpoints."""
    
    def create_payment(self, token: str, order_id: str, method: str = "CARD",
                      idempotency_key: Optional[str] = None) -> Response:
        """Create a payment for an order."""
        data = {
            "orderId": order_id,
            "method": method
        }
        headers = self.auth_headers(token)
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        
        return self.post("/payments", json_data=data, headers=headers)
    
    def get_payment(self, token: str, payment_id: str) -> Response:
        """Get a payment by ID."""
        return self.get(f"/payments/{payment_id}", headers=self.auth_headers(token))
