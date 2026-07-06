from pages.view_cart_page import ViewCartPage
from data.view_cart_data import (
    PRODUCT_ID_1,
    DETAIL_PRODUCT_ID,
    DETAIL_QUANTITY
)


# ============================================================
# TS-VC-001
# User membuka halaman cart tanpa produk
# Expected: Halaman cart tampil tanpa error
# Priority: Medium
# ============================================================

def test_ts_vc_001_open_empty_cart_without_error(driver):
    page = ViewCartPage(driver)

    page.open_cart_page()

    page.assert_cart_page_no_error()


# ============================================================
# TS-VC-002
# User melihat cart setelah menambahkan produk
# Expected: Produk tampil di cart beserta nama, harga, quantity, dan total
# Priority: High
# ============================================================

def test_ts_vc_002_view_cart_after_adding_product(driver):
    page = ViewCartPage(driver)

    page.open_products_page()

    product_name = page.get_product_name_by_id(PRODUCT_ID_1)

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_view_cart()

    page.assert_product_exists_in_cart(product_name)
    page.assert_cart_item_has_name_price_quantity_total()


# ============================================================
# TS-VC-003
# User menghapus produk dari cart
# Expected: Produk berhasil dihapus dari cart
# Priority: High
# ============================================================

def test_ts_vc_003_delete_product_from_cart(driver):
    page = ViewCartPage(driver)

    page.open_products_page()

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_view_cart()

    page.delete_first_product_from_cart()

    page.assert_cart_empty_after_delete()


# ============================================================
# TS-VC-004
# User mengecek total harga produk di cart
# Expected: Total harga sesuai dengan harga dan quantity produk
# Priority: High
# ============================================================

def test_ts_vc_004_check_total_price_in_cart(driver):
    page = ViewCartPage(driver)

    page.open_product_detail_page(DETAIL_PRODUCT_ID)

    page.set_detail_quantity(DETAIL_QUANTITY)
    page.add_product_from_detail_page()
    page.click_view_cart()

    page.assert_cart_item_has_name_price_quantity_total()
    page.assert_total_price_correct()


# ============================================================
# TS-VC-005
# User klik Proceed To Checkout dari halaman cart
# Expected: Sistem mengarahkan ke checkout atau meminta login terlebih dahulu
# Priority: High
# ============================================================

def test_ts_vc_005_click_proceed_to_checkout_from_cart(driver):
    page = ViewCartPage(driver)

    page.open_products_page()

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_view_cart()

    page.click_proceed_to_checkout()

    page.assert_checkout_or_login_prompt_visible()


# ============================================================
# TS-VC-007
# User memeriksa isi cart tetap konsisten setelah refresh halaman
# Expected: Isi cart tidak hilang/berubah secara tidak wajar setelah refresh
# Priority: Medium
# ============================================================

def test_ts_vc_007_cart_consistent_after_refresh(driver):
    page = ViewCartPage(driver)

    page.open_products_page()

    product_name = page.get_product_name_by_id(PRODUCT_ID_1)

    page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    page.click_view_cart()

    page.assert_cart_consistent_after_refresh(product_name)