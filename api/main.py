"""FastAPI application implementing OpenAPI v1 specification."""
import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse

from api.models import (
    UserRegisterRequest, UserPublic, LoginRequest, LoginResponse,
    Product, ProductCreateRequest, ProductUpdateRequest,
    Order, OrderCreateRequest, OrderStatus,
    Payment, PaymentCreateRequest, PaymentStatus,
    UserInternal, UserRole
)
from api.storage import storage
from api.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin, require_customer
)
from api.business_logic import (
    validate_and_calculate_order, reserve_stock, release_stock,
    validate_order_cancellation, validate_payment_creation, process_payment
)


app = FastAPI(
    title="Simplified E-Commerce Order & Payment API",
    version="1.0.0",
    description="Simplified REST API for a basic e-commerce domain (auth, products, orders, payments)."
)


# ========== Health ==========
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# ========== Auth Endpoints ==========
@app.post("/auth/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(request: UserRegisterRequest):
    """Register a new user."""
    # Check if user already exists
    existing_user = storage.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user
    user = UserInternal(
        id=str(uuid.uuid4()),
        email=request.email,
        password_hash=hash_password(request.password),
        role=request.role
    )
    storage.add_user(user)
    
    return UserPublic(id=user.id, email=user.email, role=user.role)


@app.post("/auth/login", response_model=LoginResponse, tags=["Auth"])
async def login(request: LoginRequest):
    """Login and get access token."""
    user = storage.get_user_by_email(request.email)
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(user.id, user.role.value)
    
    return LoginResponse(
        accessToken=access_token,
        tokenType="Bearer",
        expiresIn=3600
    )


# ========== Product Endpoints ==========
@app.get("/products", response_model=List[Product], tags=["Products"])
async def list_products():
    """List all active products. No authentication required."""
    products = storage.list_products(active_only=True)
    return products


@app.get("/products/{id}", response_model=Product, tags=["Products"])
async def get_product(id: str):
    """Get a specific product by ID. No authentication required."""
    product = storage.get_product(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {id} not found"
        )
    return product


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED, tags=["Products"])
async def create_product(request: ProductCreateRequest, user: UserInternal = Depends(require_admin)):
    """Create a new product. Admin only."""
    product = Product(
        id=str(uuid.uuid4()),
        name=request.name,
        price=request.price,
        currency=request.currency,
        stock=request.stock,
        isActive=request.isActive
    )
    storage.add_product(product)
    return product


# ========== Order Endpoints ==========
@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(request: OrderCreateRequest, user: UserInternal = Depends(require_customer)):
    """Create a new order. Customer only."""
    # Validate and calculate total
    total_amount, currency = validate_and_calculate_order(request.items)
    
    # Reserve stock
    reserve_stock(request.items)
    
    # Create order
    order = Order(
        id=str(uuid.uuid4()),
        userId=user.id,
        items=request.items,
        totalAmount=total_amount,
        currency=currency,
        status=OrderStatus.CREATED,
        createdAt=datetime.utcnow()
    )
    storage.add_order(order)
    
    return order


@app.get("/orders/{id}", response_model=Order, tags=["Orders"])
async def get_order(id: str, user: UserInternal = Depends(get_current_user)):
    """Get order by ID."""
    order = storage.get_order(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {id} not found"
        )
    
    # Users can only see their own orders (unless admin)
    if user.role != UserRole.ADMIN and order.userId != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own orders"
        )
    
    return order


@app.post("/orders/{id}/cancel", response_model=Order, tags=["Orders"])
async def cancel_order(id: str, user: UserInternal = Depends(require_customer)):
    """Cancel an order. Customer only."""
    order = storage.get_order(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {id} not found"
        )
    
    # Only order owner can cancel
    if order.userId != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own orders"
        )
    
    # Validate cancellation
    validate_order_cancellation(order)
    
    # Release stock
    release_stock(order.items)
    
    # Update order status
    order.status = OrderStatus.CANCELLED
    storage.update_order(id, order)
    
    return order


# ========== Payment Endpoints ==========
@app.post("/payments", response_model=Payment, status_code=status.HTTP_201_CREATED, tags=["Payments"])
async def create_payment(
    request: PaymentCreateRequest,
    user: UserInternal = Depends(get_current_user),
    idempotency_key: str = Header(None, alias="Idempotency-Key")
):
    """Create a payment for an order."""
    # Get order
    order = storage.get_order(request.orderId)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {request.orderId} not found"
        )
    
    # Verify user owns the order (or is admin)
    if user.role != UserRole.ADMIN and order.userId != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create payments for your own orders"
        )
    
    # Validate payment creation
    validate_payment_creation(order)
    
    # Create payment
    payment = Payment(
        id=str(uuid.uuid4()),
        orderId=request.orderId,
        amount=order.totalAmount,
        currency=order.currency,
        method=request.method,
        status=PaymentStatus.INITIATED,
        providerRef=f"PROV-{uuid.uuid4()}",
        createdAt=datetime.utcnow()
    )
    
    # Process payment (this will update payment status and order status)
    process_payment(order, payment)
    
    # Store payment
    storage.add_payment(payment)
    
    return payment


@app.get("/payments/{id}", response_model=Payment, tags=["Payments"])
async def get_payment(id: str, user: UserInternal = Depends(get_current_user)):
    """Get payment by ID."""
    payment = storage.get_payment(id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment {id} not found"
        )
    
    # Verify user owns the related order (or is admin)
    order = storage.get_order(payment.orderId)
    if order and user.role != UserRole.ADMIN and order.userId != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view payments for your own orders"
        )
    
    return payment


# ========== Startup Event ==========
@app.on_event("startup")
async def startup_event():
    """Initialize database with sample products."""
    # Create some sample products for testing
    sample_products = [
        Product(
            id=str(uuid.uuid4()),
            name="Laptop",
            price=15000.0,
            currency="TRY",
            stock=10,
            isActive=True
        ),
        Product(
            id=str(uuid.uuid4()),
            name="Mouse",
            price=150.0,
            currency="TRY",
            stock=50,
            isActive=True
        ),
        Product(
            id=str(uuid.uuid4()),
            name="Keyboard",
            price=500.0,
            currency="TRY",
            stock=30,
            isActive=True
        ),
        Product(
            id=str(uuid.uuid4()),
            name="Monitor",
            price=3000.0,
            currency="TRY",
            stock=20,
            isActive=True
        ),
    ]
    
    for product in sample_products:
        storage.add_product(product)
    
    print(f"✓ Initialized {len(sample_products)} sample products")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
