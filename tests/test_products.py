import pytest
from tests.assertions.response_assertions import assert_status_code
from tests.assertions.schema_validator import validate_product_schema, validate_error_response_schema

@pytest.mark.products
def test_prod_01_list_products(product_client):
    r = product_client.list_products()
    assert_status_code(r, 200)
    products = r.json()
    assert isinstance(products, list) and len(products) > 0
    validate_product_schema(products[0])

@pytest.mark.products
def test_prod_02_get_product_by_id(product_client):
    products = product_client.list_products().json()
    pid = products[0]["id"]

    r = product_client.get_product(pid)
    assert_status_code(r, 200)
    validate_product_schema(r.json())

@pytest.mark.products
def test_prod_04_get_missing_product_returns_404(product_client):
    r = product_client.get_product("does-not-exist")
    assert_status_code(r, 404)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "NOT_FOUND"

@pytest.mark.products
def test_prod_03_create_product_admin_only(product_client, customer_token, admin_token):
    # customer forbidden
    r1 = product_client.create_product(customer_token, name="X", price=10.0, stock=1)
    assert_status_code(r1, 403)
    validate_error_response_schema(r1.json())

    # admin ok
    r2 = product_client.create_product(admin_token, name="CheapItem", price=10.0, stock=10)
    assert_status_code(r2, 201)
    validate_product_schema(r2.json())
