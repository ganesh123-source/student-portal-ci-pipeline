import pytest
from tests.ui.pages.register_page import RegisterPage
from tests.ui.pages.dashboard_page import DashboardPage


def test_register_valid_user(driver, new_user):
    """TC01"""
    page = RegisterPage(driver)
    page.open_page()
    page.register(new_user["name"], new_user["phone"], new_user["email"], new_user["password"])

    page.wait_for_url_contains("dashboard.html")
    dashboard = DashboardPage(driver)
    assert new_user["name"] in dashboard.welcome_text()
    assert dashboard.email_text() == new_user["email"]


def test_register_existing_email(driver, registered_user):
    """TC02"""
    page = RegisterPage(driver)
    page.open_page()
    page.register("Another Name", "9876543210", registered_user["email"], "Test@1234")

    assert "already registered" in page.error_message().lower()


@pytest.mark.parametrize(
    "name, phone, email, password, expected_error",
    [
        ("", "9876543210", "a@example.com", "Test@1234", "Full name is required"),          # TC03
        ("Test User", "9876543210", "a@example.com", "abc", "Password must be 8+"),          # TC04
        ("Test User", "9876543210", "a@example.com", "abcdefgh", "Password must be 8+"),     # no number
        ("Test User", "9876543210", "not-an-email", "Test@1234", "valid email"),             # bad email
        ("Test User", "12345", "a@example.com", "Test@1234", "Phone must be 10 digits"),    # bad phone
    ],
)
def test_register_validation_errors(driver, name, phone, email, password, expected_error):
    page = RegisterPage(driver)
    page.open_page()
    page.register(name, phone, email, password)

    assert expected_error in page.error_message()