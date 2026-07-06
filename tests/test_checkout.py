from pages.register_page import RegisterPage
from pages.checkout_page import CheckoutPage
from data.register_data import VALID_REGISTER_DATA
from data.checkout_data import (
    PRODUCT_ID_1,
    ORDER_COMMENT,
    VALID_PAYMENT_DATA
)
from utils.data_generator import generate_email


def create_logged_in_account(driver):
    register_page = RegisterPage(driver)

    email = generate_email()
    data = VALID_REGISTER_DATA.copy()

    register_page.open_signup_page()
    register_page.fill_initial_signup(data["name"], email)
    register_page.fill_detail_signup_form(data)
    register_page.assert_account_created()
    register_page.continue_after_created()

    return email, data["password"]


def add_product_and_open_cart(driver):
    checkout_page = CheckoutPage(driver)

    checkout_page.open_products_page()

    product_name = checkout_page.get_product_name_by_id(PRODUCT_ID_1)

    checkout_page.add_product_by_id_from_products_page(PRODUCT_ID_1)
    checkout_page.click_view_cart()

    return product_name


def open_checkout_with_logged_in_user(driver):
    create_logged_in_account(driver)

    product_name = add_product_and_open_cart(driver)

    checkout_page = CheckoutPage(driver)
    checkout_page.click_proceed_to_checkout()
    checkout_page.assert_checkout_page_visible()

    return checkout_page, product_name


# ============================================================
# TS-CHK-001
# User melakukan checkout setelah login dan cart berisi produk
# Expected: User diarahkan ke halaman checkout
# Priority: High
# ============================================================

def test_ts_chk_001_checkout_after_login_with_product_in_cart(driver):
    create_logged_in_account(driver)

    add_product_and_open_cart(driver)

    checkout_page = CheckoutPage(driver)
    checkout_page.click_proceed_to_checkout()

    checkout_page.assert_checkout_page_visible()
    checkout_page.delete_account()


# ============================================================
# TS-CHK-002
# User checkout tanpa login
# Expected: Sistem menampilkan pilihan Register/Login
# Priority: High
# ============================================================

def test_ts_chk_002_checkout_without_login(driver):
    add_product_and_open_cart(driver)

    checkout_page = CheckoutPage(driver)
    checkout_page.click_proceed_to_checkout()

    checkout_page.assert_register_login_prompt_visible()


# ============================================================
# TS-CHK-003
# User memeriksa detail alamat dan pesanan saat checkout
# Expected: Detail alamat dan produk pesanan tampil dengan benar
# Priority: High
# ============================================================

def test_ts_chk_003_check_address_and_order_details_on_checkout(driver):
    checkout_page, product_name = open_checkout_with_logged_in_user(driver)

    checkout_page.assert_address_and_order_detail_visible(product_name)
    checkout_page.delete_account()


# ============================================================
# TS-CHK-004
# User mengisi komentar pesanan lalu klik Place Order
# Expected: User diarahkan ke halaman pembayaran
# Priority: Medium
# ============================================================

def test_ts_chk_004_fill_comment_and_place_order(driver):
    checkout_page, product_name = open_checkout_with_logged_in_user(driver)

    checkout_page.fill_order_comment(ORDER_COMMENT)
    checkout_page.click_place_order()

    checkout_page.assert_payment_page_visible()
    checkout_page.delete_account()


# ============================================================
# TS-CHK-005
# User melakukan pembayaran dengan data valid
# Expected: Sistem menampilkan pesan bahwa order berhasil dibuat
# Priority: High
# ============================================================

def test_ts_chk_005_payment_with_valid_data(driver):
    checkout_page, product_name = open_checkout_with_logged_in_user(driver)

    checkout_page.fill_order_comment(ORDER_COMMENT)
    checkout_page.click_place_order()
    checkout_page.assert_payment_page_visible()

    checkout_page.fill_payment_data(VALID_PAYMENT_DATA)
    checkout_page.click_pay_and_confirm_order()

    checkout_page.assert_order_success()

    checkout_page.continue_after_order_placed()
    checkout_page.delete_account()


# ============================================================
# TS-CHK-006
# User melakukan pembayaran dengan data kosong/tidak lengkap
# Expected: Sistem menampilkan validasi input pembayaran
# Priority: Medium
# ============================================================

def test_ts_chk_006_payment_with_empty_data(driver):
    checkout_page, product_name = open_checkout_with_logged_in_user(driver)

    checkout_page.fill_order_comment(ORDER_COMMENT)
    checkout_page.click_place_order()
    checkout_page.assert_payment_page_visible()

    checkout_page.assert_payment_required_validation_visible()

    checkout_page.delete_account()


# ============================================================
# TS-CHK-007
# User mencoba mengakses halaman checkout secara langsung saat cart kosong
# Expected: Sistem tidak mengarahkan ke proses pembayaran / menampilkan pesan cart kosong
# Priority: Medium
# ============================================================

def test_ts_chk_007_access_checkout_directly_with_empty_cart(driver):
    checkout_page = CheckoutPage(driver)

    checkout_page.open_checkout_directly()

    checkout_page.assert_checkout_not_continue_to_payment_when_cart_empty()