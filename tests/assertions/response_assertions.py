"""Response assertion helpers."""
from typing import Optional, List, Any
from requests import Response


def assert_status_code(response: Response, expected: int, message: Optional[str] = None):
    """Assert response status code."""
    msg = message or f"Expected status {expected}, got {response.status_code}"
    assert response.status_code == expected, f"{msg}\nResponse: {response.text}"


def assert_success(response: Response):
    """Assert response is successful (2xx)."""
    assert 200 <= response.status_code < 300, f"Expected success, got {response.status_code}\nResponse: {response.text}"


def assert_error_response(response: Response, expected_code: Optional[str] = None):
    """Assert response is an error with proper format."""
    data = response.json()
    assert "error" in data, "Error response must contain 'error' field"
    assert "code" in data["error"], "Error must contain 'code' field"
    assert "message" in data["error"], "Error must contain 'message' field"
    
    if expected_code:
        assert data["error"]["code"] == expected_code, \
            f"Expected error code {expected_code}, got {data['error']['code']}"


def assert_has_fields(data: dict, required_fields: List[str]):
    """Assert dictionary has all required fields."""
    missing = [field for field in required_fields if field not in data]
    assert not missing, f"Missing required fields: {missing}"


def assert_field_type(data: dict, field: str, expected_type: type):
    """Assert field has expected type."""
    assert field in data, f"Field '{field}' not found in response"
    actual_value = data[field]
    assert isinstance(actual_value, expected_type), \
        f"Field '{field}' should be {expected_type.__name__}, got {type(actual_value).__name__}"


def assert_field_value(data: dict, field: str, expected_value: Any):
    """Assert field has expected value."""
    assert field in data, f"Field '{field}' not found in response"
    actual_value = data[field]
    assert actual_value == expected_value, \
        f"Field '{field}' should be {expected_value}, got {actual_value}"
