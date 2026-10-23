from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.dashboard_page import DashboardPage


def test_login_valid(driver, registered_user):
    """TC05"""
    page = LoginPage(driver)
    page.open_page()
    page.login(registered_user["email"], registered_user["password"])

    page.wait_for_url_contains("dashboard.html")
    assert registered_user["name"] in DashboardPage(driver).welcome_text()


def test_login_wrong_password(driver, registered_user):
    """TC06"""
    page = LoginPage(driver)
    page.open_page()
    page.login(registered_user["email"], "WrongPass123")

    assert page.error_message() == "Invalid email or password"
    assert "index.html" in driver.current_url


def test_login_empty_fields(driver):
    """TC07"""
    page = LoginPage(driver)
    page.open_page()
    page.login("", "")

    assert page.error_message() == "Email and password are required"