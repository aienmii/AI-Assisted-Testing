import pytest
from playwright.sync_api import Page, expect
import time

BASE_URL = "https://www.saucedemo.com/"
PROBLEM_USER = "problem_user"
PERFORMANCE_GLITCH_USER = "performance_glitch_user"

PASSWORD = "secret_sauce"

def test_problem_user_broken_images(page: Page):

    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill(PROBLEM_USER)
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(f"{BASE_URL}inventory.html")


    first_item_image = page.locator("#item_4_img_link img")
    image_src = first_item_image.get_attribute("src")

    assert "sl-404" in image_src, f"Expected broken image 'sl-404' but got {image_src}"


def test_performance_glitch_user_delay(page: Page):

    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill(PERFORMANCE_GLITCH_USER)
    page.locator('[data-test="password"]').fill(PASSWORD)

    start_time = time.time()
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(f"{BASE_URL}inventory.html")
    end_time = time.time()

    duration = end_time - start_time

    assert duration > 2.0, f"Expected a performance delay, but login took {duration:.2f} seconds"


def test_error_user_cannot_remove_item(page: Page):

    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("error_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    remove_btn = page.locator('[data-test="remove-sauce-labs-backpack"]')
    remove_btn.click()

    expect(remove_btn).to_be_visible()
    expect(cart_badge).to_have_text("1")


def test_visual_user_layout_differences(page: Page):

    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("visual_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(f"{BASE_URL}inventory.html")

    backpack_image = page.locator("#item_4_img_link img")
    image_src = backpack_image.get_attribute("src")

    assert "sauce-backpack" not in image_src, "Expected visual bug (swapped image), but got the correct backpack image"