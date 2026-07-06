from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class RegisterPage(BasePage):
    URL = "https://automationexercise.com/login"

    SIGNUP_TITLE = (By.XPATH, "//h2[contains(text(), 'New User Signup!')]")
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    ENTER_ACCOUNT_INFO = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), "
        "'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), "
        "'ENTER ACCOUNT INFORMATION')]"
    )

    GENDER_MR = (By.ID, "id_gender1")
    PASSWORD = (By.CSS_SELECTOR, "input[data-qa='password']")
    DAYS = (By.ID, "days")
    MONTHS = (By.ID, "months")
    YEARS = (By.ID, "years")
    NEWSLETTER = (By.ID, "newsletter")
    OPTIN = (By.ID, "optin")

    FIRST_NAME = (By.CSS_SELECTOR, "input[data-qa='first_name']")
    LAST_NAME = (By.CSS_SELECTOR, "input[data-qa='last_name']")
    COMPANY = (By.CSS_SELECTOR, "input[data-qa='company']")
    ADDRESS = (By.CSS_SELECTOR, "input[data-qa='address']")
    ADDRESS2 = (By.CSS_SELECTOR, "input[data-qa='address2']")
    COUNTRY = (By.CSS_SELECTOR, "select[data-qa='country']")
    STATE = (By.CSS_SELECTOR, "input[data-qa='state']")
    CITY = (By.CSS_SELECTOR, "input[data-qa='city']")
    ZIPCODE = (By.CSS_SELECTOR, "input[data-qa='zipcode']")
    MOBILE_NUMBER = (By.CSS_SELECTOR, "input[data-qa='mobile_number']")

    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
    ACCOUNT_CREATED = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    EXISTING_EMAIL_ERROR = (
        By.XPATH,
        "//p[contains(text(), 'Email Address already exist!')]"
    )

    LOGOUT_BUTTON = (
        By.XPATH,
        "//a[contains(@href, '/logout') or contains(text(), 'Logout')]"
    )

    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGGED_IN_TEXT = (By.XPATH, "//a[contains(text(), 'Logged in as')]")

    DELETE_ACCOUNT = (
        By.XPATH,
        "//a[contains(@href, '/delete_account')]"
    )
    ACCOUNT_DELETED = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")

    def open_signup_page(self):
        self.open_url(self.URL)
        self.wait_visible(self.SIGNUP_TITLE)

    def fill_initial_signup(self, name, email):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

    def assert_enter_account_information_visible(self):
        self.wait_visible(self.ENTER_ACCOUNT_INFO)

    def fill_detail_signup_form(self, data):
        self.assert_enter_account_information_visible()

        self.click(self.GENDER_MR)
        self.type_text(self.PASSWORD, data["password"])

        Select(self.driver.find_element(*self.DAYS)).select_by_value("10")
        Select(self.driver.find_element(*self.MONTHS)).select_by_value("5")
        Select(self.driver.find_element(*self.YEARS)).select_by_value("2000")

        self.click(self.NEWSLETTER)
        self.click(self.OPTIN)

        self.type_text(self.FIRST_NAME, data["first_name"])
        self.type_text(self.LAST_NAME, data["last_name"])
        self.type_text(self.COMPANY, data["company"])
        self.type_text(self.ADDRESS, data["address"])
        self.type_text(self.ADDRESS2, data["address2"])

        Select(self.driver.find_element(*self.COUNTRY)).select_by_visible_text(data["country"])

        self.type_text(self.STATE, data["state"])
        self.type_text(self.CITY, data["city"])
        self.type_text(self.ZIPCODE, data["zipcode"])
        self.type_text(self.MOBILE_NUMBER, data["mobile_number"])

        self.click(self.CREATE_ACCOUNT_BUTTON)

    def assert_account_created(self):
        text = self.get_text(self.ACCOUNT_CREATED)
        assert "ACCOUNT CREATED" in text.upper()

    def assert_existing_email_error(self):
        text = self.get_text(self.EXISTING_EMAIL_ERROR)
        assert "Email Address already exist!" in text

    def continue_after_created(self):
        self.click(self.CONTINUE_BUTTON)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_visible(self.LOGGED_IN_TEXT)

    def delete_account(self):
        self.click(self.DELETE_ACCOUNT)
        text = self.get_text(self.ACCOUNT_DELETED)
        assert "ACCOUNT DELETED" in text.upper()
        self.click(self.CONTINUE_BUTTON)