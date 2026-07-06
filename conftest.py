import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    # Wajib untuk GitHub Actions / Linux CI
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Tambahan umum
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()