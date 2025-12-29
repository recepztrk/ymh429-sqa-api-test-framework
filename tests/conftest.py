"""Pytest configuration and fixtures."""
import os
import pytest
from tests.clients.auth_client import AuthClient
from tests.clients.product_client import ProductClient
from tests.clients.order_client import OrderClient
from tests.clients.payment_client import PaymentClient


# Base URL configuration
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="session")
def base_url():
    """Base URL for API."""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_client(base_url):
    """Auth API client."""
    return AuthClient(base_url)


@pytest.fixture(scope="session")
def product_client(base_url):
    """Product API client."""
    return ProductClient(base_url)


@pytest.fixture(scope="session")
def order_client(base_url):
    """Order API client."""
    return OrderClient(base_url)


@pytest.fixture(scope="session")
def payment_client(base_url):
    """Payment API client."""
    return PaymentClient(base_url)


@pytest.fixture(scope="function")
def test_customer_user(auth_client):
    """Create a test customer user and return credentials."""
    from tests.data.test_data import generate_customer_data
    
    user_data = generate_customer_data()
    response = auth_client.register(
        email=user_data["email"],
        password=user_data["password"],
        role=user_data["role"]
    )
    
    assert response.status_code == 201
    
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "role": user_data["role"],
        "user_data": response.json()
    }


@pytest.fixture(scope="function")
def customer_token(auth_client, test_customer_user):
    """Get access token for test customer."""
    response = auth_client.login(
        email=test_customer_user["email"],
        password=test_customer_user["password"]
    )
    
    assert response.status_code == 200
    return response.json()["accessToken"]


@pytest.fixture(scope="function")
def test_admin_user(auth_client):
    """Create a test admin user and return credentials."""
    from tests.data.test_data import generate_admin_data

    user_data = generate_admin_data()
    response = auth_client.register(
        email=user_data["email"],
        password=user_data["password"],
        role=user_data["role"],
    )
    assert response.status_code == 201, response.text

    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "role": user_data["role"],
        "user_data": response.json(),
    }


@pytest.fixture(scope="function")
def admin_token(auth_client, test_admin_user):
    """Get access token for test admin."""
    response = auth_client.login(
        email=test_admin_user["email"],
        password=test_admin_user["password"],
    )
    assert response.status_code == 200, response.text
    return response.json()["accessToken"]
