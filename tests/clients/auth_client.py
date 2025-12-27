"""Auth API client."""
from typing import Dict
from requests import Response
from tests.clients.api_client import APIClient


class AuthClient(APIClient):
    """Client for authentication endpoints."""
    
    def register(self, email: str, password: str, role: str = "customer") -> Response:
        """Register a new user."""
        data = {
            "email": email,
            "password": password,
            "role": role
        }
        return self.post("/auth/register", json_data=data)
    
    def login(self, email: str, password: str) -> Response:
        """Login and get access token."""
        data = {
            "email": email,
            "password": password
        }
        return self.post("/auth/login", json_data=data)
