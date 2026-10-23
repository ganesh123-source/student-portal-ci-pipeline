from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")
    ERROR_MSG = (By.ID, "error-msg")

    def open_page(self):
        self.open("/index.html")

    def login(self, email, password):
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def error_message(self):
        return self.wait_for_text(self.ERROR_MSG)