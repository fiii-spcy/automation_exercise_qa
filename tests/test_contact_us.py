from pages.contact_us_page import ContactUsPage
from data.contact_us_data import (
    VALID_CONTACT_DATA,
    INVALID_EMAIL_CONTACT_DATA,
    INVALID_FILE_CONTACT_DATA
)


# ============================================================
# TS-CU-001
# User mengirim pesan Contact Us dengan data valid
# Expected: Sistem menampilkan pesan sukses bahwa pesan berhasil dikirim
# Priority: High
# ============================================================

def test_ts_cu_001_submit_contact_us_with_valid_data(driver):
    page = ContactUsPage(driver)

    page.open_contact_us_page()
    page.fill_contact_form(VALID_CONTACT_DATA)
    page.submit_form_and_accept_alert()

    page.assert_success_message_visible()


# ============================================================
# TS-CU-002
# User submit form Contact Us tanpa mengisi data
# Expected: Sistem menampilkan validasi field wajib diisi
# Priority: Medium
# ============================================================

def test_ts_cu_002_submit_contact_us_with_empty_data(driver):
    page = ContactUsPage(driver)

    page.open_contact_us_page()

    page.assert_required_field_validation_visible()


# ============================================================
# TS-CU-003
# User mengisi email dengan format tidak valid
# Expected: Sistem menolak format email tidak valid
# Priority: Medium
# ============================================================

def test_ts_cu_003_submit_contact_us_with_invalid_email(driver):
    page = ContactUsPage(driver)

    page.open_contact_us_page()
    page.fill_contact_form(INVALID_EMAIL_CONTACT_DATA)

    page.assert_invalid_email_validation_visible()


# ============================================================
# TS-CU-004
# User upload file saat mengirim pesan
# Expected: File berhasil dilampirkan dan form dapat dikirim
# Priority: Medium
# ============================================================

def test_ts_cu_004_submit_contact_us_with_file_upload(driver, tmp_path):
    page = ContactUsPage(driver)

    upload_file = tmp_path / "contact_test_file.txt"
    upload_file.write_text("Ini file testing Contact Us Selenium.", encoding="utf-8")

    page.open_contact_us_page()
    page.fill_contact_form(VALID_CONTACT_DATA)
    page.upload_file(str(upload_file))
    page.submit_form_and_accept_alert()

    page.assert_success_message_visible()


# ============================================================
# TS-CU-006
# User upload file dengan format atau ukuran yang tidak sesuai
# Expected: Sistem menolak file dan menampilkan pesan error yang jelas
# Priority: Medium
# ============================================================

def test_ts_cu_006_submit_contact_us_with_invalid_file(driver, tmp_path):
    page = ContactUsPage(driver)

    invalid_file = tmp_path / "invalid_file.exe"
    invalid_file.write_text("Ini simulasi file dengan format tidak sesuai.", encoding="utf-8")

    page.open_contact_us_page()
    page.fill_contact_form(INVALID_FILE_CONTACT_DATA)
    page.upload_file(str(invalid_file))
    page.submit_form_and_accept_alert()

    page.assert_invalid_file_rejected()