import json
import os
import uuid
import pytest
from tests.api.api_client import signup, login
import allure
pytestmark = allure.feature("Auth API")

DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data.json")
with open(DATA_FILE) as f:
    INVALID_SIGNUPS = json.load(f)["invalid_signups"]


def unique_email():
    return f"test_{uuid.uuid4().hex[:10]}@example.com"


def test_signup_valid():
    email = unique_email()
    r = signup(email, "Test@1234")

    assert r.status_code == 200
    body = r.json()
    assert body["user"]["email"] == email
    assert "access_token" in body


def test_signup_duplicate_email(api_user):
    r = signup(api_user["email"], "Test@1234")

    assert r.status_code in (400, 422)
    assert "already" in r.text.lower()


@pytest.mark.parametrize("case", INVALID_SIGNUPS, ids=[c["case"] for c in INVALID_SIGNUPS])
def test_signup_invalid_data(case):
    email = case["email"].replace("{uid}", uuid.uuid4().hex[:10])
    r = signup(email, case["password"])

    assert r.status_code in case["expected_statuses"]


def test_login_valid(api_user):
    r = login(api_user["email"], api_user["password"])

    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(api_user):
    r = login(api_user["email"], "WrongPass123")

    assert r.status_code == 400
    assert "access_token" not in r.json()