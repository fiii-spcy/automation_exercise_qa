from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class LogoutPage(BasePage):
    BASE_URL = "https://automationexercise.com"
    LOGIN_URL = f"{BASE_URL}/login"

    # Dipakai sebagai simulasi halaman akun/protected page
    PROTECTED_ACCOUNT_URL = f"{BASE_URL}/delete_account"

    LOGOUT_BUTTON = (
        By.XPATH,
        "//a[contains(@href, '/logout') or contains(text(), 'Logout')]"
    )

    SIGNUP_LOGIN_MENU = (
        By.XPATH,
        "//a[contains(@href, '/login') and contains(., 'Signup / Login')]"
    )

    LOGIN_TITLE = (
        By.XPATH,
        "//h2[contains(text(), 'Login to your account')]"
    )

    SIGNUP_TITLE = (
        By.XPATH,
        "//h2[contains(text(), 'New User Signup!')]"
    )

    LOGGED_IN_AS = (
        By.XPATH,
        "//a[contains(text(), 'Logged in as')]"
    )

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    def assert_redirected_to_login_page(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: "/login" in driver.current_url
        )

        self.wait_visible(self.LOGIN_TITLE)
        self.wait_visible(self.SIGNUP_TITLE)

        assert "/login" in self.driver.current_url

    def open_home_page(self):
        self.open_url(self.BASE_URL)

    def open_protected_account_url(self):
        self.open_url(self.PROTECTED_ACCOUNT_URL)

    def is_element_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    def assert_logged_out_state(self):
        assert not self.is_element_present(self.LOGGED_IN_AS)
        assert not self.is_element_present(self.LOGOUT_BUTTON)
        assert self.is_element_present(self.SIGNUP_LOGIN_MENU)

    def assert_protected_page_redirected_to_login(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: "/login" in driver.current_url
        )

        self.wait_visible(self.LOGIN_TITLE)
        assert "/login" in self.driver.current_url