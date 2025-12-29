import pytest
from tests.assertions.response_assertions import assert_status_code
from tests.assertions.schema_validator import validate_payment_schema, validate_order_schema, validate_error_response_schema
from tests.data.test_data import create_order_items, generate_customer_data, pick_valid_product_and_qty

@pytest.mark.payments
def test_pay_02_create_payment_success(auth_client, product_client, order_client, payment_client, customer_token):
    products = product_client.list_products().json()
    pid, qty = pick_valid_product_and_qty(products)

    order_r = order_client.create_order(customer_token, create_order_items(pid, qty=qty))
    assert_status_code(order_r, 201)
    order = order_r.json()
    validate_order_schema(order)

    pay_r = payment_client.create_payment(customer_token, order_id=order["id"], method="CARD")
    assert_status_code(pay_r, 201)
    payment = pay_r.json()
    validate_payment_schema(payment)
    assert payment["status"] == "CAPTURED"

    # verify order is PAID
    order_check = order_client.get_order(customer_token, order["id"])
    assert_status_code(order_check, 200)
    assert order_check.json()["status"] == "PAID"

@pytest.mark.payments
def test_pay_07_payment_for_other_users_order_forbidden(auth_client, product_client, order_client, payment_client, customer_token):
    products = product_client.list_products().json()
    pid, qty = pick_valid_product_and_qty(products)

    order_r = order_client.create_order(customer_token, create_order_items(pid, qty=qty))
    assert_status_code(order_r, 201)
    order_id = order_r.json()["id"]

    # second user token
    user2 = generate_customer_data()
    r_reg = auth_client.register(email=user2["email"], password=user2["password"], role="customer")
    assert_status_code(r_reg, 201)
    r_login = auth_client.login(email=user2["email"], password=user2["password"])
    assert_status_code(r_login, 200)
    token2 = r_login.json()["accessToken"]

    pay_r = payment_client.create_payment(token2, order_id=order_id, method="CARD")
    assert_status_code(pay_r, 403)
    body = pay_r.json()
    validate_error_response_schema(body)
    assert body["error"]["code"] == "FORBIDDEN"
