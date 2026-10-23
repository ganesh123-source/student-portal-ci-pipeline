from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    WELCOME_MSG = (By.ID, "welcome-msg")
    USER_EMAIL = (By.ID, "user-email")
    LOGOUT_BTN = (By.ID, "logout-btn")

    def open_page(self):
        self.open("/dashboard.html")

    def welcome_text(self):
        # Page first shows "Loading...", so wait until it becomes "Welcome, ..."
        self.wait.until(lambda d: d.find_element(*self.WELCOME_MSG).text.startswith("Welcome"))
        return self.driver.find_element(*self.WELCOME_MSG).text

    def email_text(self):
        return self.wait_for_text(self.USER_EMAIL)

    def logout(self):
        self.click(self.LOGOUT_BTN)