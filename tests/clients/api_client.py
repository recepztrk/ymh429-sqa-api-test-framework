"""Base API client with request/response logging."""
import json
import logging
from typing import Optional, Dict, Any
import requests
from requests import Response


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class APIClient:
    """Base API client with logging and common functionality."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
    
    def _log_request(self, method: str, url: str, headers: Optional[Dict] = None, 
                     body: Optional[Any] = None):
        """Log HTTP request details."""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"REQUEST: {method} {url}")
        if headers:
            # Mask sensitive headers
            safe_headers = {k: ('***' if k.lower() in ['authorization', 'idempotency-key'] else v) 
                           for k, v in headers.items()}
            self.logger.info(f"Headers: {json.dumps(safe_headers, indent=2)}")
        if body:
            self.logger.info(f"Body: {json.dumps(body, indent=2)}")
    
    def _log_response(self, response: Response):
        """Log HTTP response details."""
        self.logger.info(f"\nRESPONSE: {response.status_code}")
        self.logger.info(f"Headers: {dict(response.headers)}")
        try:
            response_json = response.json()
            self.logger.info(f"Body: {json.dumps(response_json, indent=2)}")
        except:
            self.logger.info(f"Body: {response.text}")
        self.logger.info(f"{'='*80}\n")
    
    def request(self, method: str, endpoint: str, headers: Optional[Dict] = None,
                json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Response:
        """Make HTTP request with logging."""
        url = f"{self.base_url}{endpoint}"
        
        # Log request
        self._log_request(method, url, headers, json_data)
        
        # Make request
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            params=params
        )
        
        # Log response
        self._log_response(response)
        
        return response
    
    def get(self, endpoint: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Response:
        """HTTP GET request."""
        return self.request("GET", endpoint, headers=headers, params=params)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, 
             headers: Optional[Dict] = None) -> Response:
        """HTTP POST request."""
        return self.request("POST", endpoint, headers=headers, json_data=json_data)
    
    def patch(self, endpoint: str, json_data: Optional[Dict] = None,
              headers: Optional[Dict] = None) -> Response:
        """HTTP PATCH request."""
        return self.request("PATCH", endpoint, headers=headers, json_data=json_data)
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Response:
        """HTTP DELETE request."""
        return self.request("DELETE", endpoint, headers=headers)
    
    def auth_headers(self, token: str) -> Dict[str, str]:
        """Create authentication headers."""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
