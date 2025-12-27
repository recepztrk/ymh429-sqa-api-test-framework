# Project Brief (for IDE implementation support)

## 1) Objective
Develop a reusable API test automation framework for a simplified e-commerce domain and demonstrate it with a working REST API.

Primary evaluation focus: **test framework quality and reuse** (client layer, assertions, data-driven tests, reporting, CI execution). Keep the API minimal.

## 2) Domain model (minimal)
- **User**: id, email, password, role (`customer` | `admin`)
- **Product**: id, name, price, currency (default: TRY), stock, isActive
- **Order**: id, userId, items[{productId, qty}], totalAmount, currency, status (`CREATED` | `PAID` | `CANCELLED`), createdAt
- **Payment**: id, orderId, amount, currency, method (`CARD` | `TRANSFER`), status (`INITIATED` | `CAPTURED` | `FAILED` | `REFUNDED`), providerRef, createdAt

## 3) Business rules (design these to enable boundary/negative tests)
- Quantity per item: **1..10**
- Cart total: **min 50 TRY**, **max 5000 TRY**
- Stock must be sufficient when creating an order; if insufficient return **409** with code `STOCK_INSUFFICIENT`
- Order state transitions:
  - `CREATED` -> `PAID` (payment captured)
  - `CREATED` -> `CANCELLED` (cancel endpoint)
  - `PAID` cannot be cancelled (return 409 `INVALID_ORDER_STATE`)
- Payment rules:
  - Payment can be created only if order status is `CREATED`
  - Payment amount must equal order `totalAmount` (otherwise 422 `AMOUNT_MISMATCH`)
  - Optional idempotency via `Idempotency-Key` header: same key + orderId returns the original payment or 409 `DUPLICATE_PAYMENT`
- Authorization (minimum):
  - `admin`: create/update product, adjust stock
  - `customer`: list products, create/cancel own orders, create payments for own orders

## 4) API contract
- OpenAPI file: **openapi_v1.yaml** (keep updated if implementation changes)
- Endpoints (baseline):
  - GET /health (no auth)
  - POST /auth/register (no auth)
  - POST /auth/login (no auth)
  - GET /products (no auth)
  - GET /products/{id} (no auth)
  - POST /products (admin)
  - POST /orders (customer)
  - GET /orders/{id} (auth)
  - POST /orders/{id}/cancel (customer)
  - POST /payments (customer)
  - GET /payments/{id} (auth)

## 5) Error model (standardize for consistent tests)
Return JSON:
  {
    "error": { "code": "...", "message": "...", "details": [...] },
    "requestId": "uuid"
  }
Status codes guideline:
- 400: payload validation errors (`VALIDATION_ERROR`)
- 401: missing/invalid token (`UNAUTHORIZED`)
- 403: valid token but no permission (`FORBIDDEN`)
- 404: resource not found (`NOT_FOUND`)
- 409: conflicts (stock, duplicate payment, invalid state) (`CONFLICT` variants)
- 422: business rule violations (min/max cart, amount mismatch) (`BUSINESS_RULE_VIOLATION` variants)

## 6) Recommended implementation stack
- API: FastAPI + uvicorn + pydantic
- Tests: pytest + requests
- Schema validation (recommended): jsonschema
- Config: python-dotenv (optional)
- Reporting: pytest `--junitxml=...` (+ optional pytest-html)
- CI: GitHub Actions or GitLab CI

## 7) Repo layout (suggested)
api/
  app/main.py
  app/routes/ (auth.py, products.py, orders.py, payments.py)
  app/models/ (pydantic schemas)
  app/storage/ (in-memory or sqlite; keep simple)
tests/
  clients/ (BaseClient, AuthClient, ProductClient, OrderClient, PaymentClient)
  assertions/ (status_assertions.py, schema_assertions.py, business_assertions.py)
  data/ (json/yaml payloads for parametrized tests)
  schemas/ (json schemas for key responses, optional)
  test_smoke.py
  test_auth.py
  test_products.py
  test_orders.py
  test_payments.py
  conftest.py
docs/
  evidence/ (screenshots, logs, CI run references)
  diagrams/
.github/workflows/ci.yml (or .gitlab-ci.yml)

## 8) Test framework design notes
- `BaseClient` should:
  - manage base_url, headers, bearer token
  - provide `request()` wrapper returning response + parsed json
  - log request/response on failure (store under docs/evidence)
- Domain clients wrap endpoints and return typed dicts / objects.
- Assertions should be centralized (avoid repeating checks in every test).
- Data-driven tests:
  - store payloads and expected status codes in `tests/data/`
  - parametrize pytest tests reading those files
- Fixtures in conftest.py:
  - base_url, admin_token, customer_token
  - seeded product list (stable IDs to simplify tests)

## 9) Minimum test suites (must exist)
1) Smoke flow:
   register/login -> list products -> create order -> create payment -> verify order is PAID
2) Negative auth:
   missing token => 401; invalid token => 401; customer calling admin endpoint => 403
3) Boundary:
   cart total: 49, 50, 5000, 5001; qty: 0, 1, 10, 11; stock: 0/1/N and N+1 request
4) Contract:
   response schemas: required fields + type checks for Product/Order/Payment and ErrorResponse

## 10) CI expectations
- Start API in CI (uvicorn background or docker-compose)
- Run tests: `pytest -q --junitxml=reports/junit.xml`
- Upload artifacts: junit.xml (and html report if used), plus failure logs

## 11) Evidence to capture for the final report
- Local pytest output (terminal screenshot or captured log)
- CI run summary screenshot (green pipeline) and/or artifact links
- At least one example request/response log (happy) and one negative case
- Architecture diagram (can be simple box diagram)

## 12) Suggested local commands
- Run API: `uvicorn app.main:app --reload --port 8000`
- Run tests: `pytest -q`
- Run tests with report: `pytest -q --junitxml=reports/junit.xml`
