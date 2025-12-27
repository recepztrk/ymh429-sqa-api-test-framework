"""Business logic validation and rules."""
from typing import List, Tuple
from fastapi import HTTPException, status
from api.models import OrderItem, Order, OrderStatus, Payment, PaymentStatus
from api.storage import storage


# Business rule constants
MIN_CART_TOTAL = 50.0
MAX_CART_TOTAL = 5000.0
MIN_QTY = 1
MAX_QTY = 10


def validate_and_calculate_order(items: List[OrderItem]) -> Tuple[float, str]:
    """
    Validate order items and calculate total.
    Returns (total_amount, currency).
    Raises HTTPException if validation fails.
    """
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    total_amount = 0.0
    currency = "TRY"
    
    for item in items:
        # Validate quantity
        if item.qty < MIN_QTY or item.qty > MAX_QTY:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Quantity must be between {MIN_QTY} and {MAX_QTY}"
            )
        
        # Get product
        product = storage.get_product(item.productId)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.productId} not found"
            )
        
        if not product.isActive:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {item.productId} is not available"
            )
        
        # Check stock
        if product.stock < item.qty:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Insufficient stock for product {item.productId}. Available: {product.stock}, Requested: {item.qty}"
            )
        
        # Calculate total
        total_amount += product.price * item.qty
    
    # Validate cart total
    if total_amount < MIN_CART_TOTAL:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cart total must be at least {MIN_CART_TOTAL} {currency}. Current: {total_amount}"
        )
    
    if total_amount > MAX_CART_TOTAL:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cart total cannot exceed {MAX_CART_TOTAL} {currency}. Current: {total_amount}"
        )
    
    return total_amount, currency


def reserve_stock(items: List[OrderItem]) -> None:
    """
    Reserve stock for order items.
    Raises HTTPException if stock is insufficient.
    """
    reserved = []
    
    try:
        for item in items:
            success = storage.decrease_stock(item.productId, item.qty)
            if not success:
                # Rollback
                for rollback_item in reserved:
                    storage.increase_stock(rollback_item.productId, rollback_item.qty)
                
                product = storage.get_product(item.productId)
                available = product.stock if product else 0
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product {item.productId}. Available: {available}, Requested: {item.qty}"
                )
            reserved.append(item)
    except HTTPException:
        raise
    except Exception as e:
        # Rollback on any error
        for rollback_item in reserved:
            storage.increase_stock(rollback_item.productId, rollback_item.qty)
        raise


def release_stock(items: List[OrderItem]) -> None:
    """Release stock when order is cancelled."""
    for item in items:
        storage.increase_stock(item.productId, item.qty)


def validate_order_cancellation(order: Order) -> None:
    """
    Validate if order can be cancelled.
    Raises HTTPException if cancellation is not allowed.
    """
    if order.status == OrderStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel a paid order"
        )
    
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order is already cancelled"
        )


def validate_payment_creation(order: Order) -> None:
    """
    Validate if payment can be created for order.
    Raises HTTPException if payment creation is not allowed.
    """
    if order.status != OrderStatus.CREATED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot create payment for order with status {order.status}. Order must be in CREATED status."
        )
    
    # Check if payment already exists for this order
    existing_payment = storage.get_payment_by_order(order.id)
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Payment already exists for order {order.id}"
        )


def process_payment(order: Order, payment: Payment) -> None:
    """
    Process payment and update order status.
    This is a simplified version - in production, this would integrate with a payment provider.
    """
    # Validate payment amount matches order total
    if abs(payment.amount - order.totalAmount) > 0.01:  # Allow small floating point differences
        payment.status = PaymentStatus.FAILED
        storage.add_payment(payment)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Payment amount {payment.amount} does not match order total {order.totalAmount}"
        )
    
    # Mark payment as captured
    payment.status = PaymentStatus.CAPTURED
    
    # Update order status to PAID
    order.status = OrderStatus.PAID
    storage.update_order(order.id, order)
