# Test Evidence Documentation

## Evidence Artifacts Overview

This directory contains all test execution evidence for traceability and audit purposes.

### Artifacts Included

| Artifact | Description | Date | Status |
|----------|-------------|------|--------|
| `SMK-01_smoke_output.txt` | Complete console output from SMK-01 smoke test execution | 2025-12-27 | ✅ PASS |
| `ci-pipeline-success.png` | Screenshot of successful GitHub Actions CI run | 2025-12-27 | ✅ SUCCESS |

### Test Execution Summary

**Test ID**: SMK-01  
**Test Name**: End-to-End Smoke Test  
**Test Type**: E2E / Smoke  
**Execution Date**: 2025-12-27  
**Execution Time**: 0.45 seconds  
**Result**: ✅ PASSED

**Test Flow**:
1. ✅ Register new customer user
2. ✅ Login and obtain JWT token
3. ✅ List available products
4. ✅ Create order (150 TRY)
5. ✅ Create payment (CARD)
6. ✅ Verify order status changed to PAID

**Test Data**:
- User: `test_0474ec9a@example.com`
- Product: Mouse - 150.0 TRY
- Order ID: `cf2926c9-b998-4d46-b8a6-bcacde4dc00f`
- Payment ID: `cf604b07-7082-47a5-a014-c43f20af2e61`
- Payment Method: CARD
- Final Status: PAID

### Detailed Request/Response Logs

All HTTP interactions are logged in `SMK-01_smoke_output.txt` including:
- Request method, URL, headers (with sensitive data masked)
- Request body (JSON formatted)
- Response status code
- Response headers
- Response body (JSON formatted)

Example from logs:
```
2025-12-28 01:56:48 [INFO] REQUEST: POST http://127.0.0.1:8000/orders
2025-12-28 01:56:48 [INFO] Headers: {
  "Authorization": "***",
  "Content-Type": "application/json"
}
2025-12-28 01:56:48 [INFO] Body: {
  "items": [{"productId": "28ccfa4c-4f48-4eae-ad34-ff29517828a2", "qty": 1}]
}
2025-12-28 01:56:48 [INFO] RESPONSE: 201
2025-12-28 01:56:48 [INFO] Body: {
  "id": "cf2926c9-b998-4d46-b8a6-bcacde4dc00f",
  "status": "CREATED",
  "totalAmount": 150.0
}
```

### CI/CD Evidence

**Pipeline**: GitHub Actions  
**Workflow File**: `.github/workflows/ci.yml`  
**Status**: ✅ PASSING

**Pipeline Steps**:
1. ✅ Checkout code
2. ✅ Setup Python 3.11
3. ✅ Install dependencies
4. ✅ Start API server
5. ✅ Health check verification
6. ✅ Run smoke tests (`pytest -m smoke`)
7. ✅ Upload JUnit XML artifacts

**Total Pipeline Duration**: ~20 seconds

### Traceability

| Test ID | Requirement | Implementation | Evidence |
|---------|-------------|----------------|----------|
| SMK-01 | Complete purchase flow | All API endpoints | SMK-01_smoke_output.txt |
| HLTH-01 | Health check | GET /health | Included in CI pipeline |
| AUTH-01 | User registration | POST /auth/register | Step 1 in SMK-01 |
| AUTH-04 | User login | POST /auth/login | Step 2 in SMK-01 |
| PROD-01 | List products | GET /products | Step 3 in SMK-01 |
| ORD-03 | Create order | POST /orders | Step 4 in SMK-01 |
| PAY-02 | Create payment | POST /payments | Step 5 in SMK-01 |
| PAY-03 | Order status update | Business logic | Step 6 in SMK-01 |

### Validation Points

✅ **OpenAPI Compliance**: All responses match schema definitions  
✅ **Business Rules**: Cart total 150 TRY within limits (50-5000)  
✅ **Authentication**: JWT token required and validated  
✅ **State Transitions**: Order CREATED → PAID flow correct  
✅ **Data Integrity**: All IDs generated and referenced correctly  
✅ **Error Handling**: No unexpected 5xx errors  

### Environment Configuration

**Local Execution**:
- OS: macOS
- Python: 3.14 (venv)
- Base URL: http://127.0.0.1:8000
- Server: uvicorn

**CI Execution**:
- OS: ubuntu-latest
- Python: 3.11
- Base URL: http://127.0.0.1:8000 (env var)
- Server: uvicorn

### Notes

- All tests executed successfully without modifications
- No flaky tests observed (100% pass rate across multiple runs)
- Evidence demonstrates deterministic behavior
- Request/response logging enabled by default for debugging

---

**Evidence Collected By**: Recep Öztürk (22290380)  
**Course**: YMH429 Software Quality Assurance  
**Project**: API Test Automation Framework
