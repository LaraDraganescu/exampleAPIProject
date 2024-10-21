from playwright.sync_api import sync_playwright, Playwright


def expand_checkboxes(page, path):
    steps = path.split('>')

    for step in steps:
        step = step.strip()
        checkbox = page.locator(f"xpath=.//span[contains(text(), '{step}')]")
        toggle_button = checkbox.locator(".//button[@class='rct-collapse rct-collapse-btn']")
        toggle_button.click()


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elements=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')] ]")
    grup_elements.locator("xpath=.//span[contains(text(), 'Check Box')]").click()

    expand_checkboxes(page, "Home > Documents")

    browser.close()


with sync_playwright() as playwright:
    run(playwright)