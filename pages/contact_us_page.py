from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class ContactUsPage(BasePage):
    URL = "https://automationexercise.com/contact_us"

    GET_IN_TOUCH_TITLE = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), "
        "'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), "
        "'GET IN TOUCH')]"
    )

    NAME_FIELD = (
        By.CSS_SELECTOR,
        "input[data-qa='name']"
    )

    EMAIL_FIELD = (
        By.CSS_SELECTOR,
        "input[data-qa='email']"
    )

    SUBJECT_FIELD = (
        By.CSS_SELECTOR,
        "input[data-qa='subject']"
    )

    MESSAGE_FIELD = (
        By.CSS_SELECTOR,
        "textarea[data-qa='message']"
    )

    FILE_UPLOAD = (
        By.CSS_SELECTOR,
        "input[name='upload_file']"
    )

    SUBMIT_BUTTON = (
        By.CSS_SELECTOR,
        "input[data-qa='submit-button']"
    )

    SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), 'Success! Your details have been submitted successfully.')]"
    )

    HOME_BUTTON = (
        By.XPATH,
        "//span[contains(text(), 'Home')]/ancestor::a | //a[contains(text(), 'Home')]"
    )

    PAGE_BODY = (
        By.TAG_NAME,
        "body"
    )

    def open_contact_us_page(self):
        self.open_url(self.URL)
        self.wait_visible(self.GET_IN_TOUCH_TITLE)

    def fill_contact_form(self, data):
        self.type_text(self.NAME_FIELD, data["name"])
        self.type_text(self.EMAIL_FIELD, data["email"])
        self.type_text(self.SUBJECT_FIELD, data["subject"])
        self.type_text(self.MESSAGE_FIELD, data["message"])

    def upload_file(self, file_path):
        file_input = self.wait_visible(self.FILE_UPLOAD)
        file_input.send_keys(file_path)

    def click_submit_button(self):
        button = self.wait_clickable(self.SUBMIT_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def accept_alert_if_present(self):
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            pass

    def submit_form_and_accept_alert(self):
        self.click_submit_button()
        self.accept_alert_if_present()

    def get_validation_message(self, locator):
        element = self.driver.find_element(*locator)

        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def is_success_message_visible(self):
        return len(self.driver.find_elements(*self.SUCCESS_MESSAGE)) > 0

    def assert_success_message_visible(self):
        success_text = self.get_text(self.SUCCESS_MESSAGE)

        assert "Success! Your details have been submitted successfully." in success_text

    def assert_required_field_validation_visible(self):
        self.click_submit_button()

        validation_message = self.get_validation_message(self.NAME_FIELD)

        assert validation_message != ""
        assert "/contact_us" in self.driver.current_url

    def assert_invalid_email_validation_visible(self):
        self.click_submit_button()

        validation_message = self.get_validation_message(self.EMAIL_FIELD)

        assert validation_message != ""
        assert "/contact_us" in self.driver.current_url

    def assert_invalid_file_rejected(self):
        """
        Test ini dibuat sesuai expected result TS-CU-006.
        Jika website tetap menerima file invalid, maka test ini akan Failed.
        """
        body_text = self.get_text(self.PAGE_BODY).lower()

        success_visible = self.is_success_message_visible()

        assert not success_visible, (
            "Sistem masih menerima file dengan format/ukuran tidak sesuai."
        )

        error_keywords = [
            "invalid",
            "not allowed",
            "format",
            "file type",
            "file size",
            "error",
            "rejected"
        ]

        assert any(keyword in body_text for keyword in error_keywords), (
            "Sistem tidak menampilkan pesan error yang jelas untuk file invalid."
        )

    def click_home_button(self):
        self.click(self.HOME_BUTTON)

    def assert_home_page_visible(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: driver.current_url == "https://automationexercise.com/"
            or driver.current_url == "https://automationexercise.com"
        )

        assert "automationexercise.com" in self.driver.current_url