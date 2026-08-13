import re
import pytest
from playwright.sync_api import Page, expect
import time


BASE_URL = "https://www.saucedemo.com/"

VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"


def login(page: Page, username: str, password: str) -> None:
    page.goto(BASE_URL)
    page.locator("[data-test='username']").fill(username)
    page.locator("[data-test='password']").fill(password)
    page.locator("[data-test='login-button']").click()



def test_successful_login_shows_inventory(page: Page) -> None:
    login(page, VALID_USER, PASSWORD)

    expect(page).to_have_url(re.compile(r".*inventory\.html"))

    expect(page.locator(".title")).to_have_text("Products")

    products = page.locator(".inventory_item")
    expect(products).to_have_count(6)


def test_locked_out_user_cannot_login(page: Page) -> None:
    login(page, LOCKED_USER, PASSWORD)

    expect(page).to_have_url(BASE_URL)

    error = page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

def test_add_to_cart_and_complete_checkout(page: Page) -> None:
    login(page, VALID_USER, PASSWORD)

    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url(re.compile(r".*cart\.html"))
    expect(page.locator(".cart_item .inventory_item_name")).to_have_text(
        "Sauce Labs Backpack"
    )

    page.locator("[data-test='checkout']").click()
    expect(page).to_have_url(re.compile(r".*checkout-step-one\.html"))

    page.locator("[data-test='firstName']").fill("Jane")
    page.locator("[data-test='lastName']").fill("Doe")
    page.locator("[data-test='postalCode']").fill("90210")
    page.locator("[data-test='continue']").click()

    expect(page).to_have_url(re.compile(r".*checkout-step-two\.html"))
    page.locator("[data-test='finish']").click()

    expect(page).to_have_url(re.compile(r".*checkout-complete\.html"))
    expect(page.locator(".complete-header")).to_have_text(
        "Thank you for your order!"
    )

