# YMH429 - SQA API Test Framework

## Run API (local)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
