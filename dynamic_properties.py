import time
from faulthandler import is_enabled

from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=.//h5[contains(text(),'Elements')]").click()
    page.locator("xpath=.//span[contains(text(),'Dynamic Properties')]").click()

    # elements= page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    # elements.locator("xpath=.//span[contains(text(),'Dynamic Properties')]").click()

    disable_button = page.is_disabled('#enableAfter')
    if disable_button:
        print("button is disabled")
    else:
        print("not disabled")

    color_button=page.locator('#colorChange')
    class_button=color_button.get_attribute("class")
    if "text-danger" not in class_button:
        print("not found in class")
    else:
        print("found in class")

    time.sleep(5)

    is_enable=page.is_enabled('#enableAfter')
    if is_enable:
        print("button is enabled")
    else:
        print("not enabled")

    visible=page.is_visible('#visibleAfter')
    if visible:
        print("button is visible")
    else:
        print("not visible")

    changed_class=color_button.get_attribute("class")
    if "text-danger" in changed_class:
        print("found in class")
    else:
        print("not found")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)