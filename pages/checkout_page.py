from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    BASE_URL = "https://automationexercise.com"
    PRODUCTS_URL = f"{BASE_URL}/products"
    CART_URL = f"{BASE_URL}/view_cart"
    CHECKOUT_URL = f"{BASE_URL}/checkout"

    ALL_PRODUCTS_TITLE = (
        By.XPATH,
        "//h2[contains(text(), 'All Products')]"
    )

    CART_MODAL = (
        By.ID,
        "cartModal"
    )

    VIEW_CART_BUTTON = (
        By.XPATH,
        "//u[contains(text(), 'View Cart')]"
    )

    CART_ROWS = (
        By.CSS_SELECTOR,
        "#cart_info_table tbody tr"
    )

    PROCEED_TO_CHECKOUT_BUTTON = (
        By.XPATH,
        "//a[contains(text(), 'Proceed To Checkout')]"
    )

    REGISTER_LOGIN_LINK = (
        By.XPATH,
        "//u[contains(text(), 'Register / Login')]"
    )

    ADDRESS_DETAILS_TITLE = (
        By.XPATH,
        "//*[contains(text(), 'Address Details')]"
    )

    REVIEW_ORDER_TITLE = (
        By.XPATH,
        "//*[contains(text(), 'Review Your Order')]"
    )

    DELIVERY_ADDRESS = (
        By.ID,
        "address_delivery"
    )

    BILLING_ADDRESS = (
        By.ID,
        "address_invoice"
    )

    CHECKOUT_PRODUCT_NAMES = (
        By.CSS_SELECTOR,
        "td.cart_description h4 a"
    )

    CHECKOUT_PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        "td.cart_price p"
    )

    CHECKOUT_PRODUCT_QUANTITY = (
        By.CSS_SELECTOR,
        "td.cart_quantity button"
    )

    CHECKOUT_PRODUCT_TOTAL = (
        By.CSS_SELECTOR,
        "td.cart_total p"
    )

    ORDER_COMMENT = (
        By.NAME,
        "message"
    )

    PLACE_ORDER_BUTTON = (
        By.XPATH,
        "//a[contains(text(), 'Place Order')]"
    )

    NAME_ON_CARD = (
        By.CSS_SELECTOR,
        "input[data-qa='name-on-card']"
    )

    CARD_NUMBER = (
        By.CSS_SELECTOR,
        "input[data-qa='card-number']"
    )

    CVC = (
        By.CSS_SELECTOR,
        "input[data-qa='cvc']"
    )

    EXPIRY_MONTH = (
        By.CSS_SELECTOR,
        "input[data-qa='expiry-month']"
    )

    EXPIRY_YEAR = (
        By.CSS_SELECTOR,
        "input[data-qa='expiry-year']"
    )

    PAY_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-qa='pay-button']"
    )

    ORDER_PLACED = (
        By.CSS_SELECTOR,
        "h2[data-qa='order-placed']"
    )

    CONTINUE_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-qa='continue-button']"
    )

    DELETE_ACCOUNT = (
        By.XPATH,
        "//a[contains(@href, '/delete_account')]"
    )

    ACCOUNT_DELETED = (
        By.CSS_SELECTOR,
        "h2[data-qa='account-deleted']"
    )

    PAGE_BODY = (
        By.TAG_NAME,
        "body"
    )

    def normalize_text(self, text):
        return " ".join(text.split())

    def open_products_page(self):
        self.open_url(self.PRODUCTS_URL)
        self.wait_visible(self.ALL_PRODUCTS_TITLE)

    def open_cart_page(self):
        self.open_url(self.CART_URL)

        WebDriverWait(self.driver, 15).until(
            lambda driver: "/view_cart" in driver.current_url
        )

    def open_checkout_directly(self):
        self.open_url(self.CHECKOUT_URL)

    def get_product_name_by_id(self, product_id):
        locator = (
            By.XPATH,
            f"(//a[@data-product-id='{product_id}']"
            f"/ancestor::div[contains(@class, 'product-image-wrapper')]"
            f"//div[contains(@class, 'productinfo')]//p)[1]"
        )

        product_name = self.get_text(locator)
        return self.normalize_text(product_name)

    def add_product_by_id_from_products_page(self, product_id):
        locator = (
            By.XPATH,
            f"(//div[contains(@class, 'productinfo')]"
            f"//a[@data-product-id='{product_id}'])[1]"
        )

        self.click(locator)
        self.wait_visible(self.CART_MODAL)

    def click_view_cart(self):
        self.click(self.VIEW_CART_BUTTON)

        WebDriverWait(self.driver, 15).until(
            lambda driver: "/view_cart" in driver.current_url
        )

    def click_proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)

    def fill_order_comment(self, comment):
        self.type_text(self.ORDER_COMMENT, comment)

    def click_place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)

    def fill_payment_data(self, payment_data):
        self.type_text(self.NAME_ON_CARD, payment_data["name_on_card"])
        self.type_text(self.CARD_NUMBER, payment_data["card_number"])
        self.type_text(self.CVC, payment_data["cvc"])
        self.type_text(self.EXPIRY_MONTH, payment_data["expiry_month"])
        self.type_text(self.EXPIRY_YEAR, payment_data["expiry_year"])

    def click_pay_and_confirm_order(self):
        self.click(self.PAY_BUTTON)

    def get_checkout_product_names(self):
        elements = self.driver.find_elements(*self.CHECKOUT_PRODUCT_NAMES)

        return [
            self.normalize_text(element.text)
            for element in elements
            if element.text.strip()
        ]

    def get_validation_message(self, locator):
        element = self.driver.find_element(*locator)

        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def assert_checkout_page_visible(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: "/checkout" in driver.current_url
        )

        self.wait_visible(self.ADDRESS_DETAILS_TITLE)
        self.wait_visible(self.REVIEW_ORDER_TITLE)

        assert "/checkout" in self.driver.current_url

    def assert_register_login_prompt_visible(self):
        self.wait_visible(self.REGISTER_LOGIN_LINK)

        text = self.get_text(self.REGISTER_LOGIN_LINK)

        assert "Register / Login" in text

    def assert_address_and_order_detail_visible(self, expected_product_name):
        self.wait_visible(self.DELIVERY_ADDRESS)
        self.wait_visible(self.BILLING_ADDRESS)
        self.wait_visible(self.REVIEW_ORDER_TITLE)

        delivery_address_text = self.get_text(self.DELIVERY_ADDRESS)
        billing_address_text = self.get_text(self.BILLING_ADDRESS)

        assert delivery_address_text.strip() != "", "Delivery address tidak tampil."
        assert billing_address_text.strip() != "", "Billing address tidak tampil."

        product_names = self.get_checkout_product_names()
        expected_product_name = self.normalize_text(expected_product_name)

        assert expected_product_name in product_names, (
            f"Produk '{expected_product_name}' tidak tampil di checkout. "
            f"Produk yang tampil: {product_names}"
        )

        assert self.wait_visible(self.CHECKOUT_PRODUCT_PRICE).text.strip() != ""
        assert self.wait_visible(self.CHECKOUT_PRODUCT_QUANTITY).text.strip() != ""
        assert self.wait_visible(self.CHECKOUT_PRODUCT_TOTAL).text.strip() != ""

    def assert_payment_page_visible(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: "/payment" in driver.current_url
        )

        self.wait_visible(self.NAME_ON_CARD)
        self.wait_visible(self.CARD_NUMBER)
        self.wait_visible(self.CVC)
        self.wait_visible(self.EXPIRY_MONTH)
        self.wait_visible(self.EXPIRY_YEAR)
        self.wait_visible(self.PAY_BUTTON)

        assert "/payment" in self.driver.current_url

    def assert_order_success(self):
        order_placed_text = self.get_text(self.ORDER_PLACED)

        assert "ORDER PLACED" in order_placed_text.upper()

    def assert_payment_required_validation_visible(self):
        self.click_pay_and_confirm_order()

        validation_message = self.get_validation_message(self.NAME_ON_CARD)

        assert validation_message != ""
        assert "/payment" in self.driver.current_url

    def assert_checkout_not_continue_to_payment_when_cart_empty(self):
        body_text = self.get_text(self.PAGE_BODY).lower()

        assert "/payment" not in self.driver.current_url

        error_keywords = [
            "server error",
            "internal server error",
            "500 internal server error",
            "traceback",
            "sql syntax",
            "syntax error",
            "exception"
        ]

        for error_keyword in error_keywords:
            assert error_keyword not in body_text, (
                f"Halaman menampilkan error: {error_keyword}"
            )

    def continue_after_order_placed(self):
        self.click(self.CONTINUE_BUTTON)

    def delete_account(self):
        self.click(self.DELETE_ACCOUNT)

        deleted_text = self.get_text(self.ACCOUNT_DELETED)

        assert "ACCOUNT DELETED" in deleted_text.upper()

        self.click(self.CONTINUE_BUTTON)