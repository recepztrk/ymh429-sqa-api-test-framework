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

# ========== Boundary Tests (Sınır Değer) ==========

@pytest.mark.orders
def test_ord_06_qty_minimum_boundary_success(product_client, order_client, customer_token):
    """ORD-06: qty=1 (minimum) should succeed"""
    products = product_client.list_products().json()
    mouse = _get_by_name(products, "Mouse")  # 150 TRY >= 50 min

    r = order_client.create_order(customer_token, create_order_items(mouse["id"], qty=1))
    assert_status_code(r, 201)
    validate_order_schema(r.json())
    assert r.json()["items"][0]["qty"] == 1

@pytest.mark.orders
def test_ord_07_qty_maximum_boundary_success(product_client, order_client, admin_token, customer_token):
    """ORD-07: qty=10 (maximum) should succeed"""
    # Create product with enough stock and price that 10*price is within 50-5000
    p = product_client.create_product(admin_token, name="BoundaryProduct", price=100.0, stock=20).json()

    r = order_client.create_order(customer_token, create_order_items(p["id"], qty=10))
    assert_status_code(r, 201)
    validate_order_schema(r.json())
    assert r.json()["items"][0]["qty"] == 10
    assert r.json()["totalAmount"] == 1000.0  # 100 * 10

@pytest.mark.orders
def test_ord_08_qty_exceeds_maximum_returns_422(product_client, order_client, admin_token, customer_token):
    """ORD-08: qty=11 (exceeds max) should fail with 422"""
    p = product_client.create_product(admin_token, name="OverQtyProduct", price=50.0, stock=20).json()

    r = order_client.create_order(customer_token, create_order_items(p["id"], qty=11))
    assert_status_code(r, 422)
    body = r.json()
    validate_error_response_schema(body)

@pytest.mark.orders
def test_ord_09_cart_total_at_minimum_boundary(product_client, order_client, admin_token, customer_token):
    """ORD-09: cart total exactly 50 TRY should succeed"""
    p = product_client.create_product(admin_token, name="FiftyProduct", price=50.0, stock=10).json()

    r = order_client.create_order(customer_token, create_order_items(p["id"], qty=1))
    assert_status_code(r, 201)
    validate_order_schema(r.json())
    assert r.json()["totalAmount"] == 50.0

# ========== Order Cancel Tests ==========

@pytest.mark.orders
def test_ord_cancel_created_order_success(product_client, order_client, customer_token):
    """ORD-17 (catalog): Cancel CREATED order should succeed"""
    products = product_client.list_products().json()
    mouse = _get_by_name(products, "Mouse")

    # Create order
    create_r = order_client.create_order(customer_token, create_order_items(mouse["id"], qty=1))
    assert_status_code(create_r, 201)
    order_id = create_r.json()["id"]

    # Cancel order
    cancel_r = order_client.cancel_order(customer_token, order_id)
    assert_status_code(cancel_r, 200)
    validate_order_schema(cancel_r.json())
    assert cancel_r.json()["status"] == "CANCELLED"

@pytest.mark.orders
def test_ord_cancel_paid_order_returns_409(product_client, order_client, payment_client, customer_token):
    """ORD-18 (catalog): Cancel PAID order should fail with 409"""
    products = product_client.list_products().json()
    mouse = _get_by_name(products, "Mouse")

    # Create order
    create_r = order_client.create_order(customer_token, create_order_items(mouse["id"], qty=1))
    assert_status_code(create_r, 201)
    order = create_r.json()

    # Pay for order
    pay_r = payment_client.create_payment(customer_token, order_id=order["id"], method="CARD")
    assert_status_code(pay_r, 201)

    # Try to cancel paid order
    cancel_r = order_client.cancel_order(customer_token, order["id"])
    assert_status_code(cancel_r, 409)
    body = cancel_r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "CONFLICT"
