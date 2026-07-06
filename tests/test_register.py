import pytest

from pages.register_page import RegisterPage
from data.register_data import VALID_REGISTER_DATA, INVALID_EMAIL_DATA
from utils.data_generator import generate_email


# ============================================================
# TS-REG-001
# Register akun baru dengan data valid
# Expected: Account Created
# Priority: High
# ============================================================

def test_ts_reg_001_register_valid_account(driver):
    page = RegisterPage(driver)

    email = generate_email()
    data = VALID_REGISTER_DATA.copy()

    page.open_signup_page()
    page.fill_initial_signup(data["name"], email)
    page.fill_detail_signup_form(data)
    page.assert_account_created()

    page.continue_after_created()
    page.delete_account()


# ============================================================
# TS-REG-002
# Register menggunakan email yang sudah terdaftar
# Expected: Email Address already exist!
# Priority: High
# ============================================================

def test_ts_reg_002_register_with_existing_email(driver):
    page = RegisterPage(driver)

    email = generate_email()
    password = VALID_REGISTER_DATA["password"]
    data = VALID_REGISTER_DATA.copy()

    # Step 1: buat akun dulu
    page.open_signup_page()
    page.fill_initial_signup(data["name"], email)
    page.fill_detail_signup_form(data)
    page.assert_account_created()

    # Step 2: lanjut lalu logout
    page.continue_after_created()
    page.logout()

    # Step 3: coba daftar ulang pakai email yang sama
    page.open_signup_page()
    page.fill_initial_signup("User Duplicate", email)
    page.assert_existing_email_error()

    # Step 4: cleanup akun
    page.open_signup_page()
    page.login(email, password)
    page.delete_account()


# ============================================================
# TS-REG-003
# Register tanpa mengisi nama atau email
# Expected: Validasi field wajib diisi
# Priority: Medium
# ============================================================

@pytest.mark.parametrize(
    "name,email,invalid_field",
    [
        ("", "valid_email@mailtest.com", RegisterPage.SIGNUP_NAME),
        ("Hashfi", "", RegisterPage.SIGNUP_EMAIL),
        ("", "", RegisterPage.SIGNUP_NAME),
    ]
)
def test_ts_reg_003_register_required_field_validation(
    driver,
    name,
    email,
    invalid_field
):
    page = RegisterPage(driver)

    page.open_signup_page()

    name_input = driver.find_element(*RegisterPage.SIGNUP_NAME)
    email_input = driver.find_element(*RegisterPage.SIGNUP_EMAIL)

    name_input.clear()
    name_input.send_keys(name)

    email_input.clear()
    email_input.send_keys(email)

    driver.find_element(*RegisterPage.SIGNUP_BUTTON).click()

    validation_message = page.get_validation_message(invalid_field)

    assert validation_message != ""
    assert "/login" in driver.current_url


# ============================================================
# TS-REG-004
# Melanjutkan isi detail akun sampai submit
# Expected: Account Created
# Priority: Medium
# ============================================================

def test_ts_reg_004_fill_detail_signup_until_submit(driver):
    page = RegisterPage(driver)

    email = generate_email()
    data = VALID_REGISTER_DATA.copy()

    page.open_signup_page()
    page.fill_initial_signup(data["name"], email)

    page.assert_enter_account_information_visible()

    page.fill_detail_signup_form(data)
    page.assert_account_created()

    page.continue_after_created()
    page.delete_account()


# ============================================================
# TS-REG-005
# Register dengan format email tidak valid
# Expected: Sistem menolak format email
# Priority: Medium
# ============================================================

@pytest.mark.parametrize("invalid_email", INVALID_EMAIL_DATA)
def test_ts_reg_005_register_with_invalid_email_format(driver, invalid_email):
    page = RegisterPage(driver)

    page.open_signup_page()

    name_input = driver.find_element(*RegisterPage.SIGNUP_NAME)
    email_input = driver.find_element(*RegisterPage.SIGNUP_EMAIL)

    name_input.clear()
    name_input.send_keys("Hashfi Invalid Email")

    email_input.clear()
    email_input.send_keys(invalid_email)

    driver.find_element(*RegisterPage.SIGNUP_BUTTON).click()

    validation_message = page.get_validation_message(RegisterPage.SIGNUP_EMAIL)

    assert validation_message != ""
    assert "/login" in driver.current_url