"""
SMK-01: End-to-end smoke test
Flow: register -> login -> list products -> create order -> create payment -> verify order PAID
"""
import pytest
from tests.assertions.response_assertions import (
    assert_status_code, assert_has_fields, assert_field_value
)
from tests.assertions.schema_validator import (
    validate_user_public_schema, validate_login_response_schema,
    validate_product_schema, validate_order_schema, validate_payment_schema
)
from tests.data.test_data import generate_customer_data, create_order_items

@pytest.mark.smoke
def test_smk_01_end_to_end_happy_flow(auth_client, product_client, order_client, payment_client):
    """
    Test ID: SMK-01
    Type: E2E
    Scenario: Complete purchase flow from registration to payment
    Expected: All steps succeed, order becomes PAID
    """
    print("\n" + "="*80)
    print("SMK-01: E2E Smoke Test - Complete Purchase Flow")
    print("="*80)
    
    # Step 1: Register a new customer
    print("\n[STEP 1] Registering new customer...")
    customer_data = generate_customer_data()
    register_response = auth_client.register(
        email=customer_data["email"],
        password=customer_data["password"],
        role="customer"
    )
    assert_status_code(register_response, 201, "Registration should succeed")
    user = register_response.json()
    validate_user_public_schema(user)
    print(f"✓ User registered: {user['email']}")
    
    # Step 2: Login to get access token
    print("\n[STEP 2] Logging in...")
    login_response = auth_client.login(
        email=customer_data["email"],
        password=customer_data["password"]
    )
    assert_status_code(login_response, 200, "Login should succeed")
    login_data = login_response.json()
    validate_login_response_schema(login_data)
    access_token = login_data["accessToken"]
    print(f"✓ Login successful, token received")
    
    # Step 3: List products
    print("\n[STEP 3] Listing products...")
    products_response = product_client.list_products()
    assert_status_code(products_response, 200, "Product list should succeed")
    products = products_response.json()
    assert isinstance(products, list), "Products should be a list"
    assert len(products) > 0, "Should have at least one product"
    
    # Validate first product schema
    validate_product_schema(products[0])
    
    # Select a product that meets cart minimum (50 TRY) and won't exceed max (5000 TRY)
    # We need a product where price * reasonable_qty is between 50 and 5000
    selected_product = None
    for product in products:
        if 50 <= product["price"] <= 5000:  # Price alone should be reasonable
            selected_product = product
            break
    
    # If no single product meets criteria, use the cheapest one
    if not selected_product:
        selected_product = min(products, key=lambda p: p["price"])
    
    print(f"✓ Found {len(products)} products")
    print(f"  Selected product: {selected_product['name']} - {selected_product['price']} {selected_product['currency']}")
    
    # Step 4: Create an order
    print("\n[STEP 4] Creating order...")
    # Calculate quantity to meet minimum cart total (50 TRY) but not exceed max (5000 TRY)
    product_price = selected_product["price"]
    min_qty = max(1, int(50 / product_price) + 1) if product_price < 50 else 1
    max_possible_qty = int(5000 / product_price)
    order_qty = min(min_qty, max_possible_qty, 10)  # Don't exceed max qty per item (10)
    
    # Make sure we meet the minimum
    if product_price * order_qty < 50:
        order_qty = min(int(50 / product_price) + 1, 10, max_possible_qty)
    
    order_items = create_order_items(selected_product["id"], qty=order_qty)
    order_response = order_client.create_order(access_token, order_items)
    assert_status_code(order_response, 201, "Order creation should succeed")
    order = order_response.json()
    validate_order_schema(order)
    assert_field_value(order, "status", "CREATED")
    print(f"✓ Order created: {order['id']}")
    print(f"  Total: {order['totalAmount']} {order['currency']}")
    print(f"  Status: {order['status']}")
    
    # Step 5: Create payment for the order
    print("\n[STEP 5] Creating payment...")
    payment_response = payment_client.create_payment(
        token=access_token,
        order_id=order["id"],
        method="CARD"
    )
    assert_status_code(payment_response, 201, "Payment creation should succeed")
    payment = payment_response.json()
    validate_payment_schema(payment)
    assert_field_value(payment, "status", "CAPTURED")
    print(f"✓ Payment created: {payment['id']}")
    print(f"  Amount: {payment['amount']} {payment['currency']}")
    print(f"  Method: {payment['method']}")
    print(f"  Status: {payment['status']}")
    
    # Step 6: Verify order is now PAID
    print("\n[STEP 6] Verifying order status...")
    order_check_response = order_client.get_order(access_token, order["id"])
    assert_status_code(order_check_response, 200, "Order retrieval should succeed")
    updated_order = order_check_response.json()
    assert_field_value(updated_order, "status", "PAID")
    print(f"✓ Order status verified: {updated_order['status']}")
    
    # Final summary
    print("\n" + "="*80)
    print("SMK-01: PASSED ✓")
    print("="*80)
    print(f"User: {user['email']}")
    print(f"Order: {order['id']} - {order['totalAmount']} {order['currency']}")
    print(f"Payment: {payment['id']} - {payment['status']}")
    print(f"Final Order Status: {updated_order['status']}")
    print("="*80 + "\n")
