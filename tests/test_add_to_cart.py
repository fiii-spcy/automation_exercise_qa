from pages.add_to_cart_page import AddToCartPage
from data.add_to_cart_data import (
    PRODUCT_ID_1,
    PRODUCT_ID_2,
    DETAIL_PRODUCT_ID,
    DETAIL_QUANTITY
)


# ============================================================
# TS-ATC-001
# User menambahkan satu produk ke cart
# Expected: Produk berhasil ditambahkan ke cart
# Priority: High
# ============================================================

def test_ts_atc_001_add_one_product_to_cart(driver):
    page = AddToCartPage(driver)

    page.open_products_page()

    product_name = page.get_product_name_by_id(PRODUCT_ID_1)

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_view_cart()

    page.assert_product_exists_in_cart(product_name)


# ============================================================
# TS-ATC-002
# User menambahkan lebih dari satu produk ke cart
# Expected: Semua produk yang dipilih muncul di cart
# Priority: High
# ============================================================

def test_ts_atc_002_add_multiple_products_to_cart(driver):
    page = AddToCartPage(driver)

    page.open_products_page()

    first_product_name = page.get_product_name_by_id(PRODUCT_ID_1)
    second_product_name = page.get_product_name_by_id(PRODUCT_ID_2)

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_continue_shopping()

    page.add_product_by_id_from_products_page(PRODUCT_ID_2)
    page.click_view_cart()

    page.assert_product_exists_in_cart(first_product_name)
    page.assert_product_exists_in_cart(second_product_name)
    page.assert_cart_has_minimum_products(2)


# ============================================================
# TS-ATC-003
# User menambahkan produk dari halaman detail produk
# Expected: Produk berhasil masuk ke cart
# Priority: Medium
# ============================================================

def test_ts_atc_003_add_product_from_detail_page(driver):
    page = AddToCartPage(driver)

    page.open_product_detail_page(DETAIL_PRODUCT_ID)

    product_name = page.get_detail_product_name()

    page.add_product_from_detail_page()
    page.click_view_cart()

    page.assert_product_exists_in_cart(product_name)


# ============================================================
# TS-ATC-005
# User mengubah quantity di halaman detail produk sebelum klik Add to Cart
# Expected: Produk masuk ke cart dengan quantity sesuai input user
# Priority: Medium
# ============================================================

def test_ts_atc_005_add_product_with_custom_quantity_from_detail_page(driver):
    page = AddToCartPage(driver)

    page.open_product_detail_page(DETAIL_PRODUCT_ID)

    product_name = page.get_detail_product_name()

    page.set_detail_quantity(DETAIL_QUANTITY)
    page.add_product_from_detail_page()
    page.click_view_cart()

    page.assert_product_exists_in_cart(product_name)
    page.assert_cart_quantity_equals(DETAIL_QUANTITY)

