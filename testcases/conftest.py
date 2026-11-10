import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

import allure
import pytest
from selenium import webdriver

from utils.config_loader import get_config


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    d = webdriver.Chrome(options=options)
    yield d
    if getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed:
        path = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
        os.makedirs(path, exist_ok=True)
        file = os.path.join(path, f"{request.node.name}.png")
        d.save_screenshot(file)
        allure.attach.file(file, name="failure", attachment_type=allure.attachment_type.PNG)
    d.quit()


@pytest.fixture
def api_client():
    from common.api_client import AdminApiClient

    cfg = get_config()["api"]
    return AdminApiClient(cfg["base_url"], cfg.get("timeout", 10))


@pytest.fixture
def db():
    from common.db_client import DbClient

    client = DbClient()
    yield client
    client.close()
