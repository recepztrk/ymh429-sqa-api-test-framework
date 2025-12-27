"""Pydantic models matching OpenAPI v1 specification."""
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


# ========== Enums ==========
class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, Enum):
    CARD = "CARD"
    TRANSFER = "TRANSFER"


class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


# ========== Error Models ==========
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[List[dict]] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
    requestId: Optional[str] = None


# ========== Auth Models ==========
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: Optional[int] = 3600


# ========== Product Models ==========
class Product(BaseModel):
    id: str
    name: str
    price: float = Field(..., ge=0)
    currency: str = "TRY"
    stock: int = Field(..., ge=0)
    isActive: bool = True


class ProductCreateRequest(BaseModel):
    name: str
    price: float = Field(..., ge=0)
    currency: str = "TRY"
    stock: int = Field(..., ge=0)
    isActive: bool = True


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    isActive: Optional[bool] = None


# ========== Order Models ==========
class OrderItem(BaseModel):
    productId: str
    qty: int = Field(..., ge=1, le=10)


class Order(BaseModel):
    id: str
    userId: str
    items: List[OrderItem]
    totalAmount: float = Field(..., ge=0)
    currency: str = "TRY"
    status: OrderStatus
    createdAt: datetime


class OrderCreateRequest(BaseModel):
    items: List[OrderItem] = Field(..., min_length=1)


# ========== Payment Models ==========
class Payment(BaseModel):
    id: str
    orderId: str
    amount: float = Field(..., ge=0)
    currency: str = "TRY"
    method: PaymentMethod
    status: PaymentStatus
    providerRef: str
    createdAt: datetime


class PaymentCreateRequest(BaseModel):
    orderId: str
    method: PaymentMethod


# ========== Internal Storage Models ==========
class UserInternal(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    role: UserRole
