from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://automationexercise.com/login"

    LOGIN_TITLE = (By.XPATH, "//h2[contains(text(), 'Login to your account')]")

    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")

    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(), 'Logged in as')]")

    LOGIN_ERROR = (
        By.XPATH,
        "//p[contains(text(), 'Your email or password is incorrect!')]"
    )

    LOGOUT_BUTTON = (
        By.XPATH,
        "//a[contains(@href, '/logout') or contains(text(), 'Logout')]"
    )

    DELETE_ACCOUNT = (
        By.XPATH,
        "//a[contains(@href, '/delete_account')]"
    )

    ACCOUNT_DELETED = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def open_login_page(self):
        self.open_url(self.URL)
        self.wait_visible(self.LOGIN_TITLE)

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def assert_login_success(self):
        text = self.get_text(self.LOGGED_IN_AS)
        assert "Logged in as" in text

    def assert_login_error(self):
        text = self.get_text(self.LOGIN_ERROR)
        assert "Your email or password is incorrect!" in text

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    def delete_account(self):
        self.click(self.DELETE_ACCOUNT)
        text = self.get_text(self.ACCOUNT_DELETED)
        assert "ACCOUNT DELETED" in text.upper()
        self.click(self.CONTINUE_BUTTON)