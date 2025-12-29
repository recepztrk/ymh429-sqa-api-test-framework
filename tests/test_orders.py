import pytest
from tests.assertions.response_assertions import assert_status_code
from tests.assertions.schema_validator import validate_order_schema, validate_error_response_schema
from tests.data.test_data import create_order_items

def _get_by_name(products, name):
    for p in products:
        if p["name"] == name:
            return p
    return products[0]

@pytest.mark.orders
def test_ord_03_create_order_success(product_client, order_client, customer_token):
    products = product_client.list_products().json()
    mouse = _get_by_name(products, "Mouse")

    r = order_client.create_order(customer_token, create_order_items(mouse["id"], qty=1))
    assert_status_code(r, 201)
    validate_order_schema(r.json())
    assert r.json()["status"] == "CREATED"

@pytest.mark.orders
def test_ord_17_order_total_exceeds_max_returns_422(product_client, order_client, customer_token):
    products = product_client.list_products().json()
    laptop = _get_by_name(products, "Laptop")  # 15000 > 5000

    r = order_client.create_order(customer_token, create_order_items(laptop["id"], qty=1))
    assert_status_code(r, 422)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "VALIDATION_ERROR"

@pytest.mark.orders
def test_ord_05_insufficient_stock_returns_409(product_client, order_client, admin_token, customer_token):
    # create limited stock product
    p = product_client.create_product(admin_token, name="LimitedStock", price=100.0, stock=1).json()

    r = order_client.create_order(customer_token, create_order_items(p["id"], qty=2))
    assert_status_code(r, 409)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "CONFLICT"

@pytest.mark.orders
def test_ord_18_below_min_cart_total_returns_422(product_client, order_client, admin_token, customer_token):
    # create cheap product so total < 50
    p = product_client.create_product(admin_token, name="TooCheap", price=10.0, stock=10).json()

    r = order_client.create_order(customer_token, create_order_items(p["id"], qty=1))  # total=10
    assert_status_code(r, 422)
    body = r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "VALIDATION_ERROR"
