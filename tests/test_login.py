from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from data.register_data import VALID_REGISTER_DATA
from data.login_data import (
    VALID_LOGIN_PASSWORD,
    WRONG_PASSWORD,
    UNREGISTERED_EMAIL,
    UNREGISTERED_PASSWORD
)
from utils.data_generator import generate_email


def create_account_then_logout(driver):
    register_page = RegisterPage(driver)

    email = generate_email()
    data = VALID_REGISTER_DATA.copy()
    data["password"] = VALID_LOGIN_PASSWORD

    register_page.open_signup_page()
    register_page.fill_initial_signup(data["name"], email)
    register_page.fill_detail_signup_form(data)
    register_page.assert_account_created()

    register_page.continue_after_created()
    register_page.logout()

    return email, data["password"]


# ============================================================
# TS-LOG-001
# Login menggunakan email dan password valid
# Expected: User berhasil login dan muncul teks "Logged in as username"
# Priority: High
# ============================================================

def test_ts_log_001_login_with_valid_email_and_password(driver):
    email, password = create_account_then_logout(driver)

    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(email, password)

    login_page.assert_login_success()

    login_page.delete_account()


# ============================================================
# TS-LOG-002
# Login menggunakan email valid tetapi password salah
# Expected: Sistem menampilkan pesan error login
# Priority: High
# ============================================================

def test_ts_log_002_login_with_valid_email_wrong_password(driver):
    email, password = create_account_then_logout(driver)

    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(email, WRONG_PASSWORD)

    login_page.assert_login_error()

    # Cleanup akun
    login_page.login(email, password)
    login_page.assert_login_success()
    login_page.delete_account()


# ============================================================
# TS-LOG-003
# Login menggunakan email yang tidak terdaftar
# Expected: Sistem menampilkan pesan error email/password salah
# Priority: High
# ============================================================

def test_ts_log_003_login_with_unregistered_email(driver):
    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(UNREGISTERED_EMAIL, UNREGISTERED_PASSWORD)

    login_page.assert_login_error()


# ============================================================
# TS-LOG-004
# Login tanpa mengisi email dan password
# Expected: Sistem menampilkan validasi input wajib diisi
# Priority: Medium
# ============================================================

def test_ts_log_004_login_with_empty_email_and_password(driver):
    login_page = LoginPage(driver)

    login_page.open_login_page()

    driver.find_element(*LoginPage.LOGIN_BUTTON).click()

    validation_message = login_page.get_validation_message(LoginPage.LOGIN_EMAIL)

    assert validation_message != ""
    assert "/login" in driver.current_url