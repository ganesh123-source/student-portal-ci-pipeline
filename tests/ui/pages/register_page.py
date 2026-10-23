from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    FULL_NAME = (By.ID, "full-name")
    PHONE = (By.ID, "phone")
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    REGISTER_BTN = (By.ID, "register-btn")
    ERROR_MSG = (By.ID, "error-msg")

    def open_page(self):
        self.open("/register.html")

    def register(self, name, phone, email, password):
        self.type(self.FULL_NAME, name)
        self.type(self.PHONE, phone)
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.REGISTER_BTN)

    def error_message(self):
        return self.wait_for_text(self.ERROR_MSG)