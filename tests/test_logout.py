from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from data.register_data import VALID_REGISTER_DATA
from utils.data_generator import generate_email


def create_account_then_logout(driver):
    register_page = RegisterPage(driver)

    email = generate_email()
    data = VALID_REGISTER_DATA.copy()
    password = data["password"]

    register_page.open_signup_page()
    register_page.fill_initial_signup(data["name"], email)
    register_page.fill_detail_signup_form(data)
    register_page.assert_account_created()

    register_page.continue_after_created()
    register_page.logout()

    return email, password


def login_with_existing_account(driver, email, password):
    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(email, password)
    login_page.assert_login_success()


def cleanup_account(driver, email, password):
    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(email, password)
    login_page.assert_login_success()
    login_page.delete_account()


# ============================================================
# TS-LOUT-001
# User melakukan logout setelah berhasil login
# Expected: User berhasil logout dan diarahkan ke halaman Login/Signup
# Priority: High
# ============================================================

def test_ts_lout_001_logout_after_successful_login(driver):
    email, password = create_account_then_logout(driver)

    login_with_existing_account(driver, email, password)

    logout_page = LogoutPage(driver)
    logout_page.logout()
    logout_page.assert_redirected_to_login_page()

    cleanup_account(driver, email, password)


# ============================================================
# TS-LOUT-003
# User mengakses kembali halaman setelah logout
# Expected: Sistem tidak lagi menampilkan status login user
# Priority: Medium
# ============================================================

def test_ts_lout_003_access_page_after_logout(driver):
    email, password = create_account_then_logout(driver)

    login_with_existing_account(driver, email, password)

    logout_page = LogoutPage(driver)
    logout_page.logout()
    logout_page.assert_redirected_to_login_page()

    logout_page.open_home_page()
    logout_page.assert_logged_out_state()

    cleanup_account(driver, email, password)


# ============================================================
# TS-LOUT-004
# User mencoba mengakses halaman akun langsung lewat URL setelah logout
# Expected: Sistem mengarahkan user ke halaman Login
# Priority: Medium
# ============================================================

def test_ts_lout_004_access_account_page_url_after_logout(driver):
    email, password = create_account_then_logout(driver)

    login_with_existing_account(driver, email, password)

    logout_page = LogoutPage(driver)
    logout_page.logout()
    logout_page.assert_redirected_to_login_page()

    logout_page.open_protected_account_url()
    logout_page.assert_protected_page_redirected_to_login()

    cleanup_account(driver, email, password)