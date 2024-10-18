from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Buttons')]").click()

    # page.locator("#doubleClickBtn").dblclick()
    page.get_by_text("Double Click Me").dblclick()
    page.get_by_text("Right Click Me").click(button="right")
    # page.get_by_role("button", name="Click Me").click()
    # page.click(".//button[text()='Click Me']")
    page.locator("xpath=.//button[text()='Click Me']").click()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)