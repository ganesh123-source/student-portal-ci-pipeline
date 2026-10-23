import os
import socket
import subprocess
import sys
import time
import uuid

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
def driver():
    options = Options()
    if os.getenv("HEADLESS") == "1":     # needed later for the pipeline
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    d = webdriver.Edge(options=options)
    yield d
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