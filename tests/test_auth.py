import pytest
from tests.assertions.response_assertions import assert_status_code
from tests.assertions.schema_validator import (
    validate_user_public_schema,
    validate_login_response_schema,
    validate_error_response_schema,
)
from tests.data.test_data import generate_customer_data

@pytest.mark.auth
def test_auth_01_register_success(auth_client):
    data = generate_customer_data()
    r = auth_client.register(email=data["email"], password=data["password"], role="customer")
    assert_status_code(r, 201)
    validate_user_public_schema(r.json())

@pytest.mark.auth
def test_auth_02_register_invalid_email_returns_422(auth_client):
    r = auth_client.register(email="not-an-email", password="password123", role="customer")
    assert_status_code(r, 422)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "VALIDATION_ERROR"

@pytest.mark.auth
def test_auth_03_register_duplicate_email_returns_400(auth_client):
    data = generate_customer_data()
    r1 = auth_client.register(email=data["email"], password=data["password"], role="customer")
    assert_status_code(r1, 201)

    r2 = auth_client.register(email=data["email"], password=data["password"], role="customer")
    assert_status_code(r2, 400)
    body = r2.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "BAD_REQUEST"

@pytest.mark.auth
def test_auth_04_login_success(auth_client, test_customer_user):
    r = auth_client.login(email=test_customer_user["email"], password=test_customer_user["password"])
    assert_status_code(r, 200)
    validate_login_response_schema(r.json())

@pytest.mark.auth
def test_auth_05_login_wrong_password_returns_401(auth_client, test_customer_user):
    r = auth_client.login(email=test_customer_user["email"], password="wrong-password")
    assert_status_code(r, 401)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "UNAUTHORIZED"
