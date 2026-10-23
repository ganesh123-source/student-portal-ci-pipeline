import os
import socket
import subprocess
import sys
import time
import uuid
import allure

import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options

from tests.api.api_client import delete_test_users
from tests.ui.pages.register_page import RegisterPage
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.dashboard_page import DashboardPage

PORT = 5500
APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")


def _port_open(port):
    with socket.socket() as s:
        return s.connect_ex(("localhost", port)) == 0


@pytest.fixture(scope="session", autouse=True)
def app_server():
    if _port_open(PORT):          # you already started it yourself
        yield
        return
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--directory", APP_DIR],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(20):
        if _port_open(PORT):
            break
        time.sleep(0.5)
    yield
    proc.terminate()


@pytest.fixture
def driver(request):
    options = Options()
    if os.getenv("HEADLESS") == "1":     # needed later for the pipeline
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    d = webdriver.Edge(options=options)
    yield d

    # After the test: if it failed, attach a screenshot to the report
    result = getattr(request.node, "rep_call", None)
    if result is not None and result.failed:
        allure.attach(
            d.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    d.quit()


@pytest.fixture
def new_user():
    return {
        "name": "Test User",
        "phone": "9876543210",
        "email": f"test_{uuid.uuid4().hex[:10]}@example.com",
        "password": "Test@1234",
    }


@pytest.fixture
def registered_user(driver, new_user):
    register = RegisterPage(driver)
    register.open_page()
    register.register(new_user["name"], new_user["phone"], new_user["email"], new_user["password"])
    dashboard = DashboardPage(driver)
    dashboard.welcome_text()             # wait until registration is done
    dashboard.logout()
    LoginPage(driver).wait_for_url_contains("index.html")
    return new_user

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_users():
    delete_test_users()      # clear leftovers from older runs
    yield
    delete_test_users()      # clear users created by this run

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)