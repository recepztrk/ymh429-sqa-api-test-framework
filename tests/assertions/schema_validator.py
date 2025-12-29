"""Schema validation helpers."""
from typing import List, Dict, Any
from requests import Response


def validate_user_public_schema(data: dict):
    """Validate UserPublic schema."""
    required_fields = ["id", "email", "role"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert isinstance(data["id"], str), "id must be string"
    assert isinstance(data["email"], str), "email must be string"
    assert data["role"] in ["customer", "admin"], f"Invalid role: {data['role']}"


def validate_login_response_schema(data: dict):
    """Validate LoginResponse schema."""
    required_fields = ["accessToken", "tokenType"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert isinstance(data["accessToken"], str), "accessToken must be string"
    assert isinstance(data["tokenType"], str), "tokenType must be string"
    assert len(data["accessToken"]) > 0, "accessToken cannot be empty"


def validate_product_schema(data: dict):
    """Validate Product schema."""
    required_fields = ["id", "name", "price", "currency", "stock", "isActive"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert isinstance(data["id"], str), "id must be string"
    assert isinstance(data["name"], str), "name must be string"
    assert isinstance(data["price"], (int, float)), "price must be number"
    assert isinstance(data["currency"], str), "currency must be string"
    assert isinstance(data["stock"], int), "stock must be integer"
    assert isinstance(data["isActive"], bool), "isActive must be boolean"


def validate_order_schema(data: dict):
    """Validate Order schema."""
    required_fields = ["id", "userId", "items", "totalAmount", "currency", "status", "createdAt"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert isinstance(data["id"], str), "id must be string"
    assert isinstance(data["userId"], str), "userId must be string"
    assert isinstance(data["items"], list), "items must be array"
    assert isinstance(data["totalAmount"], (int, float)), "totalAmount must be number"
    assert isinstance(data["currency"], str), "currency must be string"
    assert data["status"] in ["CREATED", "PAID", "CANCELLED"], f"Invalid status: {data['status']}"
    assert isinstance(data["createdAt"], str), "createdAt must be string"
    
    # Validate order items
    for item in data["items"]:
        assert "productId" in item, "OrderItem must have productId"
        assert "qty" in item, "OrderItem must have qty"


def validate_payment_schema(data: dict):
    """Validate Payment schema."""
    required_fields = ["id", "orderId", "amount", "currency", "method", "status", "createdAt"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert isinstance(data["id"], str), "id must be string"
    assert isinstance(data["orderId"], str), "orderId must be string"
    assert isinstance(data["amount"], (int, float)), "amount must be number"
    assert isinstance(data["currency"], str), "currency must be string"
    assert data["method"] in ["CARD", "TRANSFER"], f"Invalid method: {data['method']}"
    assert data["status"] in ["INITIATED", "CAPTURED", "FAILED", "REFUNDED"], f"Invalid status: {data['status']}"
    assert isinstance(data["createdAt"], str), "createdAt must be string"


def validate_error_response_schema(data: dict):
    """Validate ErrorResponse schema."""
    assert "error" in data, "Missing 'error' object"
    assert "requestId" in data, "Missing 'requestId'"

    err = data["error"]
    for field in ["code", "message", "details"]:
        assert field in err, f"Missing error.{field}"

    assert isinstance(err["code"], str), "error.code must be string"
    assert isinstance(err["message"], str), "error.message must be string"
    # details may be None or list
    assert (err["details"] is None) or isinstance(err["details"], list), "error.details must be null or list"
    assert (data["requestId"] is None) or isinstance(data["requestId"], str), "requestId must be string or null"
