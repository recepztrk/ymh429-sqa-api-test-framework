import pytest
import requests
from tests.assertions.response_assertions import assert_status_code

@pytest.mark.health
def test_hlth_01_health_ok(base_url):
    r = requests.get(f"{base_url}/health")
    assert_status_code(r, 200)
    assert r.json() == {"status": "ok"}

