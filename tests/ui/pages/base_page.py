from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.config import BASE_URL


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, path):
        self.driver.get(BASE_URL + path)

    def type(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_for_text(self, locator):
        """Wait until the element has some text, then return it."""
        self.wait.until(lambda d: d.find_element(*locator).text.strip() != "")
        return self.driver.find_element(*locator).text

    def wait_for_url_contains(self, part):
        self.wait.until(EC.url_contains(part))