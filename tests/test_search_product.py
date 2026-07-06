import pytest

from pages.search_product_page import SearchProductPage
from data.search_product_data import (
    VALID_SEARCH_KEYWORD,
    UNAVAILABLE_SEARCH_KEYWORD,
    EMPTY_SEARCH_KEYWORD,
    CASE_INSENSITIVE_KEYWORDS,
    SPECIAL_CHARACTER_KEYWORD,
    LONG_INJECTION_KEYWORD
)


# ============================================================
# TS-SP-001
# User mencari produk dengan keyword valid
# Expected: Produk yang sesuai keyword ditampilkan
# Priority: High
# ============================================================

def test_ts_sp_001_search_product_with_valid_keyword(driver):
    page = SearchProductPage(driver)

    page.open_products_page()
    page.search_product(VALID_SEARCH_KEYWORD)

    page.assert_products_relevant_to_keyword(VALID_SEARCH_KEYWORD)


# ============================================================
# TS-SP-002
# User mencari produk dengan keyword yang tidak tersedia
# Expected: Sistem tidak menampilkan produk yang tidak sesuai / hasil kosong
# Priority: Medium
# ============================================================

def test_ts_sp_002_search_product_with_unavailable_keyword(driver):
    page = SearchProductPage(driver)

    page.open_products_page()
    page.search_product(UNAVAILABLE_SEARCH_KEYWORD)

    page.assert_searched_products_page_visible()
    page.assert_no_unrelated_product_displayed(UNAVAILABLE_SEARCH_KEYWORD)
    page.assert_page_not_error()


# ============================================================
# TS-SP-003
# User melakukan pencarian dengan input kosong
# Expected: Sistem tetap berada di halaman produk atau menampilkan daftar produk
# Priority: Low
# ============================================================

#def test_ts_sp_003_search_product_with_empty_input(driver):
    #page = SearchProductPage(driver)

    #page.open_products_page()
    #page.search_product(EMPTY_SEARCH_KEYWORD)

    #page.assert_empty_search_stable()#


# ============================================================
# TS-SP-004
# User mencari produk dengan huruf besar/kecil berbeda
# Expected: Sistem tetap menampilkan produk relevan / case-insensitive
# Priority: Medium
# ============================================================

@pytest.mark.parametrize(
    "keyword",
    [
        CASE_INSENSITIVE_KEYWORDS["lowercase"],
        CASE_INSENSITIVE_KEYWORDS["uppercase"],
        CASE_INSENSITIVE_KEYWORDS["mixedcase"]
    ]
)
def test_ts_sp_004_search_product_case_insensitive(driver, keyword):
    page = SearchProductPage(driver)

    page.open_products_page()
    page.search_product(keyword)

    page.assert_products_relevant_to_keyword("shirt")


# ============================================================
# TS-SP-005
# User mencari produk dengan karakter khusus
# Expected: Sistem tidak error dan menampilkan hasil kosong atau pesan yang sesuai
# Priority: Medium
# ============================================================

def test_ts_sp_005_search_product_with_special_characters(driver):
    page = SearchProductPage(driver)

    page.open_products_page()
    page.search_product(SPECIAL_CHARACTER_KEYWORD)

    page.assert_search_stable_for_invalid_input()


# ============================================================
# TS-SP-006
# User mencari produk dengan string sangat panjang / pola injection sederhana
# Expected: Sistem stabil, tidak error, dan tidak mengeksekusi input sebagai query
# Priority: Medium
# ============================================================

def test_ts_sp_006_search_product_with_long_injection_pattern(driver):
    page = SearchProductPage(driver)

    page.open_products_page()
    page.search_product(LONG_INJECTION_KEYWORD)

    page.assert_search_stable_for_invalid_input()