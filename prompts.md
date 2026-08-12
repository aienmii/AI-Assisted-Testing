# Prompts

## Query 1

Your task is to write 3 automated tests for https://www.saucedemo.com/ using Python , pytest, and Playwright. Ensure that all tests can be executed successfully.
Credentials are:
Accepted usernames are:
standard_user
locked_out_user
problem_user
performance_glitch_user
error_user
visual_user
Password for all users:
secret_sauce

## Answer 1

Here are 3 automated tests for [SauceDemo](https://www.saucedemo.com/) using Python, `pytest`, and `playwright`.

These tests cover three distinct scenarios:

1. **Successful Login:** Logging in with a valid standard user.
2. **Locked Out User:** Verifying the error message when a locked-out user attempts to log in.
3. **Add to Cart functionality:** Logging in and verifying that adding an item to the cart updates the cart badge.

### Prerequisites

Before running the tests, you'll need to install `pytest-playwright` and the necessary browser binaries. Run these commands in your terminal:

```bash
pip install pytest-playwright
playwright install

```

### The Test Code (`test_saucedemo.py`)

Create a file named `test_saucedemo.py` and paste the following code into it:

```python
import re
from playwright.sync_api import Page, expect

# --- Constants ---
BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"

def test_successful_login(page: Page):
    """
    Test that the standard_user can log in successfully 
    and is redirected to the inventory page.
    """
    page.goto(BASE_URL)
    
    # Fill in credentials
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill(PASSWORD)
    
    # Click login
    page.locator("[data-test='login-button']").click()
    
    # Assertions
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(page.locator(".title")).to_have_text("Products")

def test_locked_out_user(page: Page):
    """
    Test that a locked out user cannot log in and 
    sees the appropriate error message.
    """
    page.goto(BASE_URL)
    
    # Fill in credentials for locked out user
    page.locator("[data-test='username']").fill("locked_out_user")
    page.locator("[data-test='password']").fill(PASSWORD)
    
    # Click login
    page.locator("[data-test='login-button']").click()
    
    # Assertions
    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

def test_add_item_to_cart(page: Page):
    """
    Test that a logged-in user can add an item to the cart 
    and the cart badge updates accordingly.
    """
    # Login first
    page.goto(BASE_URL)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill(PASSWORD)
    page.locator("[data-test='login-button']").click()
    
    # Ensure we are on the inventory page
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    
    # Add 'Sauce Labs Backpack' to the cart
    add_to_cart_button = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
    add_to_cart_button.click()
    
    # Assertions: Check if the cart badge displays '1'
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_be_visible()
    expect(cart_badge).to_have_text("1")
    
    # Assertions: Check if the button changed to 'Remove'
    remove_button = page.locator("[data-test='remove-sauce-labs-backpack']")
    expect(remove_button).to_be_visible()
    expect(remove_button).to_have_text("Remove")

```

### How to Run the Tests

To run the tests, open your terminal in the directory where you saved `test_saucedemo.py` and execute:

```bash
# Run tests in headless mode (no browser UI)
pytest test_saucedemo.py

# Run tests in headed mode (so you can watch the browser)
pytest test_saucedemo.py --headed

# Run tests with a slight delay so you can see what's happening
pytest test_saucedemo.py --headed --slowmo 500

```

### Why this structure?

* **`page` fixture:** We are using Playwright's built-in `page` fixture for pytest. This automatically launches a browser context, creates a page, passes it to the test, and cleans it up afterward.
* **`expect` assertions:** Playwright's `expect` library includes auto-retrying assertions. This means if a page takes a fraction of a second to load the cart badge, the test will smartly wait (up to a timeout limit) rather than failing instantly, resulting in non-flaky tests.
* **`data-test` attributes:** SauceDemo provides robust `data-test` attributes specifically designed for automated testing. This avoids brittle selectors like XPath or complex CSS chains.

## Query 2 

write tests for 
problem_user 
performance_glitch_user 
error_user 
visual_user 
Password for all users: 
secret_sauce

Here are the automated tests for the remaining users. Each of these users was created by the Sauce Demo developers to intentionally exhibit specific bugs or behaviors for QA practice.

These tests are designed to verify those exact intentionally broken behaviors (e.g., verifying that the `error_user` fails to remove items, or that the `performance_glitch_user` causes a delay).

### The Test File (`test_special_users.py`)

```python
import pytest
from playwright.sync_api import Page, expect
import time

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"

def test_problem_user_broken_images(page: Page):
    """
    The 'problem_user' has broken image links (replaced with a dog image 'sl-404')
    and several broken buttons. This test verifies the broken images bug.
    """
    page.goto(BASE_URL)
    
    # Login as problem_user
    page.locator('[data-test="username"]').fill("problem_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()
    
    # Assert successful login
    expect(page).to_have_url(f"{BASE_URL}inventory.html")
    
    # The first item (Sauce Labs Backpack) should have a broken image link
    # 'sl-404' is the filename of the dog image used for broken links on this site
    first_item_image = page.locator("#item_4_img_link img")
    image_src = first_item_image.get_attribute("src")
    
    assert "sl-404" in image_src, f"Expected broken image 'sl-404' but got {image_src}"

def test_performance_glitch_user_delay(page: Page):
    """
    The 'performance_glitch_user' logs in successfully but simulates a slow network 
    or backend delay (takes about 5 seconds). 
    Playwright's auto-wait handles this natively, but we can measure it to prove the glitch.
    """
    page.goto(BASE_URL)
    
    page.locator('[data-test="username"]').fill("performance_glitch_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    
    start_time = time.time()
    page.locator('[data-test="login-button"]').click()
    
    # Wait for the inventory page to load
    expect(page).to_have_url(f"{BASE_URL}inventory.html")
    end_time = time.time()
    
    duration = end_time - start_time
    # Assert that the login took longer than 2 seconds (the artificial delay)
    assert duration > 2.0, f"Expected a performance delay, but login took {duration:.2f} seconds"

def test_error_user_cannot_remove_item(page: Page):
    """
    The 'error_user' triggers JavaScript/UI errors. One notable bug is that once 
    an item is added to the cart, clicking the 'Remove' button does nothing.
    """
    page.goto(BASE_URL)
    
    page.locator('[data-test="username"]').fill("error_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()
    
    # Add backpack to cart
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    
    # Verify it was added
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")
    
    # Attempt to remove the item
    remove_btn = page.locator('[data-test="remove-sauce-labs-backpack"]')
    remove_btn.click()
    
    # Assert the bug: The button is STILL 'Remove' and the cart badge is STILL '1'
    # (If this were a standard_user, the button would revert to 'Add to cart' and badge would disappear)
    expect(remove_btn).to_be_visible()
    expect(cart_badge).to_have_text("1")

def test_visual_user_layout_differences(page: Page):
    """
    The 'visual_user' has CSS layout issues and swapped images (e.g., the backpack 
    image shows a shirt instead). We verify the swapped image source here.
    Note: For true visual testing, Playwright's snapshot feature 
    (`expect(page).to_have_screenshot()`) is typically used.
    """
    page.goto(BASE_URL)
    
    page.locator('[data-test="username"]').fill("visual_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()
    
    # Verify successful login
    expect(page).to_have_url(f"{BASE_URL}inventory.html")
    
    # The visual_user has a bug where the backpack image is swapped with the 
    # Sauce Labs Fleece Jacket (or similar).
    # A standard user's backpack image src ends with 'sauce-backpack-1200x1500.0a0b85a3.jpg'
    backpack_image = page.locator("#item_4_img_link img")
    image_src = backpack_image.get_attribute("src")
    
    # Assert that the image source is NOT the correct backpack image
    assert "sauce-backpack" not in image_src, "Expected visual bug (swapped image), but got the correct backpack image"

```

### Execution

Run these alongside your other tests using the standard `pytest` command:

```bash
pytest test_special_users.py -v

```

*(Adding the `-v` flag provides verbose output so you can clearly see the name of each passing test).*