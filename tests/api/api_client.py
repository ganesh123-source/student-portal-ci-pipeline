import requests
from tests.config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY

TIMEOUT = 15

ANON_HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Content-Type": "application/json",
}

ADMIN_HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}


def user_headers(token):
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def signup(email, password):
    return requests.post(f"{SUPABASE_URL}/auth/v1/signup",
                         headers=ANON_HEADERS,
                         json={"email": email, "password": password},
                         timeout=TIMEOUT)


def login(email, password):
    return requests.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
                         headers=ANON_HEADERS,
                         json={"email": email, "password": password},
                         timeout=TIMEOUT)


def create_profile(token, user_id, full_name, phone=None):
    return requests.post(f"{SUPABASE_URL}/rest/v1/profiles",
                         headers=user_headers(token),
                         json={"id": user_id, "full_name": full_name, "phone": phone},
                         timeout=TIMEOUT)


def get_profiles(token=None):
    headers = user_headers(token) if token else ANON_HEADERS
    return requests.get(f"{SUPABASE_URL}/rest/v1/profiles?select=*",
                        headers=headers, timeout=TIMEOUT)


def delete_user(user_id):
    return requests.delete(f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
                           headers=ADMIN_HEADERS, timeout=TIMEOUT)


def delete_test_users(prefix="test_"):
    """Delete every user whose email starts with the prefix (UI and API test users)."""
    ids = []
    page = 1
    while True:
        r = requests.get(f"{SUPABASE_URL}/auth/v1/admin/users",
                         headers=ADMIN_HEADERS,
                         params={"page": page, "per_page": 100},
                         timeout=TIMEOUT)
        users = r.json().get("users", [])
        if not users:
            break
        ids += [u["id"] for u in users if (u.get("email") or "").startswith(prefix)]
        page += 1
    for user_id in ids:
        delete_user(user_id)