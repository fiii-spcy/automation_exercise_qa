from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ViewCartPage(BasePage):
    BASE_URL = "https://automationexercise.com"
    PRODUCTS_URL = f"{BASE_URL}/products"
    CART_URL = f"{BASE_URL}/view_cart"
    PRODUCT_DETAIL_URL = f"{BASE_URL}/product_details"

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

    CONTINUE_SHOPPING_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Continue Shopping')]"
    )

    CART_ROWS = (
        By.CSS_SELECTOR,
        "#cart_info_table tbody tr"
    )

    CART_PRODUCT_NAMES = (
        By.CSS_SELECTOR,
        "td.cart_description h4 a"
    )

    CART_PRICE = (
        By.CSS_SELECTOR,
        "td.cart_price p"
    )

    CART_QUANTITY = (
        By.CSS_SELECTOR,
        "td.cart_quantity button"
    )

    CART_TOTAL = (
        By.CSS_SELECTOR,
        "td.cart_total p"
    )

    CART_DELETE_BUTTON = (
        By.CSS_SELECTOR,
        "a.cart_quantity_delete"
    )

    PROCEED_TO_CHECKOUT_BUTTON = (
        By.XPATH,
        "//a[contains(text(), 'Proceed To Checkout')]"
    )

    CHECKOUT_MODAL = (
        By.ID,
        "checkoutModal"
    )

    REGISTER_LOGIN_LINK_IN_MODAL = (
        By.XPATH,
        "//u[contains(text(), 'Register / Login')]"
    )

    PRODUCT_DETAIL_NAME = (
        By.CSS_SELECTOR,
        ".product-information h2"
    )

    PRODUCT_DETAIL_QUANTITY = (
        By.ID,
        "quantity"
    )

    PRODUCT_DETAIL_ADD_TO_CART = (
        By.CSS_SELECTOR,
        "button.cart"
    )

    PAGE_BODY = (
        By.TAG_NAME,
        "body"
    )

    def normalize_text(self, text):
        return " ".join(text.split())

    def extract_number(self, text):
        cleaned_text = "".join(char for char in text if char.isdigit())
        return int(cleaned_text) if cleaned_text else 0

    def open_cart_page(self):
        self.open_url(self.CART_URL)

        WebDriverWait(self.driver, 15).until(
            lambda driver: "/view_cart" in driver.current_url
        )

    def open_products_page(self):
        self.open_url(self.PRODUCTS_URL)
        self.wait_visible(self.ALL_PRODUCTS_TITLE)

    def open_product_detail_page(self, product_id):
        self.open_url(f"{self.PRODUCT_DETAIL_URL}/{product_id}")
        self.wait_visible(self.PRODUCT_DETAIL_NAME)

    def get_product_name_by_id(self, product_id):
        locator = (
            By.XPATH,
            f"(//a[@data-product-id='{product_id}']"
            f"/ancestor::div[contains(@class, 'product-image-wrapper')]"
            f"//div[contains(@class, 'productinfo')]//p)[1]"
        )

        return self.normalize_text(self.get_text(locator))

    def add_product_by_id_from_products_page(self, product_id):
        locator = (
            By.XPATH,
            f"(//div[contains(@class, 'productinfo')]"
            f"//a[@data-product-id='{product_id}'])[1]"
        )

        self.click(locator)
        self.wait_visible(self.CART_MODAL)

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)

        WebDriverWait(self.driver, 10).until(
            lambda driver: not self.is_cart_modal_visible()
        )

    def click_view_cart(self):
        self.click(self.VIEW_CART_BUTTON)

        WebDriverWait(self.driver, 15).until(
            lambda driver: "/view_cart" in driver.current_url
        )

    def is_cart_modal_visible(self):
        elements = self.driver.find_elements(*self.CART_MODAL)
        return len(elements) > 0 and elements[0].is_displayed()

    def get_cart_rows(self):
        return self.driver.find_elements(*self.CART_ROWS)

    def get_cart_row_count(self):
        return len(self.get_cart_rows())

    def get_cart_product_names(self):
        elements = self.driver.find_elements(*self.CART_PRODUCT_NAMES)

        return [
            self.normalize_text(element.text)
            for element in elements
            if element.text.strip()
        ]

    def get_first_cart_price(self):
        text = self.get_text(self.CART_PRICE)
        return self.extract_number(text)

    def get_first_cart_quantity(self):
        text = self.get_text(self.CART_QUANTITY)
        return self.extract_number(text)

    def get_first_cart_total(self):
        text = self.get_text(self.CART_TOTAL)
        return self.extract_number(text)

    def delete_first_product_from_cart(self):
        initial_count = self.get_cart_row_count()

        self.click(self.CART_DELETE_BUTTON)

        WebDriverWait(self.driver, 15).until(
            lambda driver: len(driver.find_elements(*self.CART_ROWS)) < initial_count
            or "Cart is empty" in driver.find_element(*self.PAGE_BODY).text
        )

    def click_proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)

    def set_detail_quantity(self, quantity):
        quantity_input = self.wait_visible(self.PRODUCT_DETAIL_QUANTITY)
        quantity_input.clear()
        quantity_input.send_keys(quantity)

    def add_product_from_detail_page(self):
        self.click(self.PRODUCT_DETAIL_ADD_TO_CART)
        self.wait_visible(self.CART_MODAL)

    def assert_cart_page_no_error(self):
        body_text = self.get_text(self.PAGE_BODY).lower()

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
                f"Halaman cart menampilkan error: {error_keyword}"
            )

        assert "/view_cart" in self.driver.current_url

    def assert_product_exists_in_cart(self, expected_product_name):
        expected_product_name = self.normalize_text(expected_product_name)
        cart_product_names = self.get_cart_product_names()

        assert expected_product_name in cart_product_names, (
            f"Produk '{expected_product_name}' tidak ditemukan di cart. "
            f"Produk di cart: {cart_product_names}"
        )

    def assert_cart_item_has_name_price_quantity_total(self):
        assert self.get_cart_row_count() > 0, "Cart kosong, tidak ada produk."

        product_names = self.get_cart_product_names()
        price = self.get_first_cart_price()
        quantity = self.get_first_cart_quantity()
        total = self.get_first_cart_total()

        assert len(product_names) > 0, "Nama produk tidak tampil di cart."
        assert price > 0, "Harga produk tidak tampil atau bernilai 0."
        assert quantity > 0, "Quantity produk tidak tampil atau bernilai 0."
        assert total > 0, "Total harga produk tidak tampil atau bernilai 0."

    def assert_cart_empty_after_delete(self):
        assert self.get_cart_row_count() == 0, (
            f"Produk belum terhapus. Jumlah row cart: {self.get_cart_row_count()}"
        )

    def assert_total_price_correct(self):
        price = self.get_first_cart_price()
        quantity = self.get_first_cart_quantity()
        total = self.get_first_cart_total()

        expected_total = price * quantity

        assert total == expected_total, (
            f"Total harga tidak sesuai. "
            f"Price: {price}, Quantity: {quantity}, "
            f"Expected Total: {expected_total}, Actual Total: {total}"
        )

    def assert_checkout_or_login_prompt_visible(self):
        current_url = self.driver.current_url

        modal_visible = len(self.driver.find_elements(*self.CHECKOUT_MODAL)) > 0
        login_link_visible = len(self.driver.find_elements(*self.REGISTER_LOGIN_LINK_IN_MODAL)) > 0

        checkout_page_opened = "/checkout" in current_url

        assert checkout_page_opened or modal_visible or login_link_visible, (
            "Sistem tidak mengarahkan ke checkout dan tidak menampilkan prompt login."
        )

    def assert_cart_consistent_after_refresh(self, expected_product_name):
        expected_product_name = self.normalize_text(expected_product_name)

        self.driver.refresh()

        WebDriverWait(self.driver, 15).until(
            lambda driver: "/view_cart" in driver.current_url
        )

        self.assert_product_exists_in_cart(expected_product_name)
        self.assert_cart_item_has_name_price_quantity_total()