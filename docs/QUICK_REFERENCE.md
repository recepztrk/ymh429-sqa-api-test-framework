# Quick Reference Guide

## Running the Project

### Start API Server
```bash
cd "/Users/recepozturk/Desktop/SQA Project"
source venv/bin/activate
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### Run Tests

**Smoke test only**:
```bash
source venv/bin/activate
pytest -m smoke -v -s
```

**All tests**:
```bash
pytest -v
```

**With HTML report**:
```bash
pytest -m smoke --html=report.html --self-contained-html
```

**Save test output**:
```bash
pytest -m smoke -v | tee docs/evidence/test-run-$(date +%Y%m%d-%H%M%S).txt
```

## Project Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### API Endpoints

**Health check**:
```bash
curl http://127.0.0.1:8000/health
```

**Register user**:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","role":"customer"}'
```

**Login**:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**List products** (no auth):
```bash
curl http://127.0.0.1:8000/products
```

**Create order** (requires token):
```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"productId":"PRODUCT_ID","qty":1}]}'
```

## File Locations

- **API Code**: `api/main.py`
- **Tests**: `tests/test_smoke.py`
- **OpenAPI Spec**: `openapi_v1.yaml`
- **Test Catalog**: `TEST_CATALOG.md`
- **Evidence**: `docs/evidence/`
- **Final Report**: `docs/FINAL_REPORT.md`
- **CI Workflow**: `.github/workflows/ci.yml`

## Common Tasks

### Update dependencies
```bash
pip freeze > requirements.txt
```

### Run specific test
```bash
pytest tests/test_smoke.py::test_smk_01_end_to_end_happy_flow -v
```

### Clear pytest cache
```bash
rm -rf .pytest_cache
rm -rf tests/__pycache__
```

### View OpenAPI docs
Start API server, then visit: http://127.0.0.1:8000/docs

## Troubleshooting

**Port already in use**:
```bash
lsof -ti :8000 | xargs kill -9
```

**pytest not found**:
```bash
source venv/bin/activate
pip install pytest
```

**Import errors**:
```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
```

## Git Commands

```bash
# Check status
git status

# Commit evidence
git add docs/evidence/
git commit -m "Add test evidence"

# Push to GitHub
git push origin main

# View CI status
# Visit: https://github.com/recepztrk/ymh429-sqa-api-test-framework/actions
```
