from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.dashboard_page import DashboardPage


def test_logout(driver, registered_user):
    """TC08"""
    login = LoginPage(driver)
    login.open_page()
    login.login(registered_user["email"], registered_user["password"])

    dashboard = DashboardPage(driver)
    dashboard.welcome_text()
    dashboard.logout()

    login.wait_for_url_contains("index.html")
    assert "index.html" in driver.current_url


def test_dashboard_blocked_when_logged_out(driver):
    """TC09: the guard at the door"""
    dashboard = DashboardPage(driver)
    dashboard.open_page()

    dashboard.wait_for_url_contains("index.html")
    assert "index.html" in driver.current_url