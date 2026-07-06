from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class AddToCartPage(BasePage):
    BASE_URL = "https://automationexercise.com"
    PRODUCTS_URL = f"{BASE_URL}/products"
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

    CART_QUANTITY = (
        By.CSS_SELECTOR,
        "td.cart_quantity button"
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

    def normalize_text(self, text):
        """
        Merapikan teks agar perbedaan spasi tidak membuat test gagal.
        Contoh:
        'Men  Tshirt' menjadi 'Men Tshirt'
        """
        return " ".join(text.split())

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

    def get_cart_product_names(self):
        elements = self.driver.find_elements(*self.CART_PRODUCT_NAMES)

        return [
            self.normalize_text(element.text)
            for element in elements
            if element.text.strip()
        ]

    def get_cart_row_count(self):
        return len(self.driver.find_elements(*self.CART_ROWS))

    def get_cart_quantity(self):
        quantity_element = self.wait_visible(self.CART_QUANTITY)
        return self.normalize_text(quantity_element.text)

    def get_detail_product_name(self):
        product_name = self.get_text(self.PRODUCT_DETAIL_NAME)
        return self.normalize_text(product_name)

    def set_detail_quantity(self, quantity):
        quantity_input = self.wait_visible(self.PRODUCT_DETAIL_QUANTITY)
        quantity_input.clear()
        quantity_input.send_keys(quantity)

    def add_product_from_detail_page(self):
        self.click(self.PRODUCT_DETAIL_ADD_TO_CART)
        self.wait_visible(self.CART_MODAL)

    def assert_product_exists_in_cart(self, expected_product_name):
        expected_product_name = self.normalize_text(expected_product_name)
        cart_product_names = self.get_cart_product_names()

        assert len(cart_product_names) > 0, "Cart kosong, tidak ada produk yang muncul."

        assert expected_product_name in cart_product_names, (
            f"Produk '{expected_product_name}' tidak ditemukan di cart. "
            f"Produk di cart: {cart_product_names}"
        )

    def assert_cart_has_minimum_products(self, minimum_count):
        row_count = self.get_cart_row_count()

        assert row_count >= minimum_count, (
            f"Jumlah produk di cart tidak sesuai. "
            f"Expected minimal: {minimum_count}, Actual: {row_count}"
        )

    def assert_cart_quantity_equals(self, expected_quantity):
        actual_quantity = self.get_cart_quantity()

        assert actual_quantity == str(expected_quantity), (
            f"Quantity tidak sesuai. "
            f"Expected: {expected_quantity}, Actual: {actual_quantity}"
        )