import uuid
import pytest
from tests.api.api_client import signup


@pytest.fixture
def api_user():
    """Creates a fresh user through the API and returns its details."""
    email = f"test_{uuid.uuid4().hex[:10]}@example.com"
    password = "Test@1234"
    r = signup(email, password)
    assert r.status_code == 200, r.text
    body = r.json()
    return {
        "email": email,
        "password": password,
        "id": body["user"]["id"],
        "token": body["access_token"],
    }