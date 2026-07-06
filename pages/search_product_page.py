from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchProductPage(BasePage):
    BASE_URL = "https://automationexercise.com"
    PRODUCTS_URL = f"{BASE_URL}/products"

    PRODUCTS_MENU = (
        By.XPATH,
        "//a[contains(@href, '/products')]"
    )

    ALL_PRODUCTS_TITLE = (
        By.XPATH,
        "//h2[contains(text(), 'All Products')]"
    )

    SEARCH_INPUT = (
        By.ID,
        "search_product"
    )

    SEARCH_BUTTON = (
        By.ID,
        "submit_search"
    )

    SEARCHED_PRODUCTS_TITLE = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), "
        "'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), "
        "'SEARCHED PRODUCTS')]"
    )

    PRODUCT_NAME_LIST = (
        By.CSS_SELECTOR,
        ".features_items .productinfo p"
    )

    PRODUCT_CARD_LIST = (
        By.CSS_SELECTOR,
        ".features_items .product-image-wrapper"
    )

    PAGE_BODY = (
        By.TAG_NAME,
        "body"
    )

    def open_products_page(self):
        self.open_url(self.PRODUCTS_URL)
        self.wait_visible(self.ALL_PRODUCTS_TITLE)

    def search_product(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def assert_searched_products_page_visible(self):
        self.wait_visible(self.SEARCHED_PRODUCTS_TITLE)

    def get_product_names(self):
        elements = self.driver.find_elements(*self.PRODUCT_NAME_LIST)
        return [
            element.text.strip()
            for element in elements
            if element.text.strip()
        ]

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_CARD_LIST))

    def assert_products_relevant_to_keyword(self, keyword):
        self.assert_searched_products_page_visible()

        product_names = self.get_product_names()

        assert len(product_names) > 0, "Tidak ada produk yang tampil pada hasil pencarian valid."

        relevant_products = [
            product_name
            for product_name in product_names
            if keyword.lower() in product_name.lower()
        ]

        assert len(relevant_products) > 0, (
            f"Tidak ada produk yang relevan dengan keyword '{keyword}'. "
            f"Produk yang tampil: {product_names}"
        )

    def assert_no_unrelated_product_displayed(self, keyword):
        self.assert_searched_products_page_visible()

        product_names = self.get_product_names()

        for product_name in product_names:
            assert keyword.lower() in product_name.lower(), (
                f"Produk tidak sesuai tetap muncul: {product_name}"
            )

    def assert_still_on_products_page(self):
        assert "/products" in self.driver.current_url

    def assert_page_not_error(self):
        body_text = self.get_text(self.PAGE_BODY).lower()

        error_keywords = [
            "server error",
            "internal server error",
            "500 internal server error",
            "http error 500",
            "traceback",
            "sql syntax",
            "syntax error",
            "exception"
        ]

        for error_keyword in error_keywords:
            assert error_keyword not in body_text, (
                f"Halaman menampilkan error: {error_keyword}"
            )

    def assert_empty_search_stable(self):
        self.assert_still_on_products_page()
        self.assert_page_not_error()

    def assert_search_stable_for_invalid_input(self):
        self.assert_still_on_products_page()
        self.assert_page_not_error()
        self.assert_searched_products_page_visible()
