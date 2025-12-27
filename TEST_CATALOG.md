# API Test Catalog (v1)

This catalog is intended to be implemented as pytest tests (data-driven where possible). IDs can be used in the final report for traceability.

## Global assumptions
- Currency: TRY
- Cart total limits: min 50, max 5000
- Qty per item: 1..10
- Error model: { error: { code, message, details }, requestId }

---

## A. Health

| ID | Type | Endpoint | Scenario | Expected |
|---|---|---|---|---|
| HLTH-01 | Functional | GET /health | Service responds OK | 200 + {status: ok} |

---

## B. Auth

| ID | Type | Endpoint | Scenario | Expected |
|---|---|---|---|---|
| AUTH-01 | Functional | POST /auth/register | Valid customer registration | 201 + UserPublic |
| AUTH-02 | Negative | POST /auth/register | Invalid email | 400 + ErrorResponse(code=VALIDATION_ERROR) |
| AUTH-03 | Negative | POST /auth/register | Password too short (<8) | 400 + ErrorResponse |
| AUTH-04 | Functional | POST /auth/login | Valid login | 200 + accessToken |
| AUTH-05 | Negative | POST /auth/login | Wrong password | 401 + ErrorResponse(code=UNAUTHORIZED) |
| AUTH-06 | Contract | POST /auth/login | Response schema validation | accessToken present, string |

---

## C. Products

| ID | Type | Endpoint | Scenario | Expected |
|---|---|---|---|---|
| PROD-01 | Functional | GET /products | List products (no auth) | 200 + [Product] |
| PROD-02 | Contract | GET /products | Product schema required fields | id,name,price,currency,stock |
| PROD-03 | Functional | GET /products/{id} | Existing product | 200 + Product |
| PROD-04 | Negative | GET /products/{id} | Non-existent product | 404 + ErrorResponse(code=NOT_FOUND) |
| PROD-05 | Security | POST /products | Unauthenticated create | 401 |
| PROD-06 | Security | POST /products | Customer role tries create | 403 |
| PROD-07 | Functional | POST /products | Admin creates product | 201 + Product |
| PROD-08 | Negative | POST /products | Admin creates with negative price | 400 |
| PROD-09 | Boundary | POST /products | Admin creates with stock=0 | 201 + stock=0 |

---

## D. Orders

| ID | Type | Endpoint | Scenario | Expected |
|---|---|---|---|---|
| ORD-01 | Security | POST /orders | Unauthenticated order create | 401 |
| ORD-02 | Security | POST /orders | Admin role tries order create (optional policy) | 403 or 201 (document decision) |
| ORD-03 | Functional | POST /orders | Customer creates order (happy) | 201 + Order(status=CREATED) |
| ORD-04 | Contract | POST /orders | Order schema required fields | id,userId,items,totalAmount,status |
| ORD-05 | Negative | POST /orders | Missing items | 400 |
| ORD-06 | Boundary | POST /orders | qty=1 | 201 |
| ORD-07 | Boundary | POST /orders | qty=10 | 201 |
| ORD-08 | Boundary | POST /orders | qty=11 | 400 or 422 (document decision) |
| ORD-09 | Boundary | POST /orders | Cart total = 50 | 201 |
| ORD-10 | Boundary | POST /orders | Cart total = 49 | 422 (BUSINESS_RULE_VIOLATION) |
| ORD-11 | Boundary | POST /orders | Cart total = 5000 | 201 |
| ORD-12 | Boundary | POST /orders | Cart total = 5001 | 422 |
| ORD-13 | Boundary | POST /orders | Stock exactly sufficient | 201 |
| ORD-14 | Negative | POST /orders | Stock insufficient (request N+1) | 409 (STOCK_INSUFFICIENT) |
| ORD-15 | Functional | GET /orders/{id} | Fetch created order | 200 |
| ORD-16 | Negative | GET /orders/{id} | Non-existent order | 404 |
| ORD-17 | Functional | POST /orders/{id}/cancel | Cancel CREATED order | 200 + status=CANCELLED |
| ORD-18 | Negative | POST /orders/{id}/cancel | Cancel PAID order | 409 (INVALID_ORDER_STATE) |

---

## E. Payments

| ID | Type | Endpoint | Scenario | Expected |
|---|---|---|---|---|
| PAY-01 | Security | POST /payments | Unauthenticated payment create | 401 |
| PAY-02 | Functional | POST /payments | Pay for CREATED order (happy) | 201 + Payment(status=CAPTURED) |
| PAY-03 | Functional | POST /payments | After payment, order becomes PAID | GET /orders/{id} => status=PAID |
| PAY-04 | Negative | POST /payments | Pay for CANCELLED order | 409 (INVALID_ORDER_STATE) |
| PAY-05 | Negative | POST /payments | Pay non-existent order | 404 |
| PAY-06 | Contract | POST /payments | Payment response schema | id,orderId,amount,method,status |
| PAY-07 | Negative | POST /payments | Duplicate payment for same order (no idempotency) | 409 (DUPLICATE_PAYMENT) |
| PAY-08 | Idempotency | POST /payments | Same Idempotency-Key repeats | returns same payment or 409 (document decision) |
| PAY-09 | Functional | GET /payments/{id} | Fetch payment | 200 |
| PAY-10 | Negative | GET /payments/{id} | Non-existent payment | 404 |

---

## F. Smoke (end-to-end)

| ID | Type | Scenario | Expected |
|---|---|---|---|
| SMK-01 | E2E | register -> login -> list products -> create order -> create payment -> verify order PAID | All steps succeed, no unexpected 5xx |
