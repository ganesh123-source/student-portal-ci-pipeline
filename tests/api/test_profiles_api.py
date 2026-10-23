import uuid
from tests.api.api_client import create_profile, get_profiles


def test_create_own_profile(api_user):
    r = create_profile(api_user["token"], api_user["id"], "API Tester", "9876543210")

    assert r.status_code == 201
    assert r.json()[0]["full_name"] == "API Tester"


def test_read_own_profile(api_user):
    create_profile(api_user["token"], api_user["id"], "API Tester")
    r = get_profiles(api_user["token"])

    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["id"] == api_user["id"]


def test_cannot_create_profile_for_another_user(api_user):
    other_id = str(uuid.uuid4())
    r = create_profile(api_user["token"], other_id, "Hacker")

    assert r.status_code == 403


def test_anonymous_user_sees_no_profiles(api_user):
    create_profile(api_user["token"], api_user["id"], "API Tester")
    r = get_profiles()          # no login token

    assert r.status_code == 200
    assert r.json() == []


def test_profile_without_name_is_rejected(api_user):
    r = create_profile(api_user["token"], api_user["id"], None)

    assert r.status_code == 400