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

