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

    page.get_by_text("Color Change").click()
    # page.click('#simpleLink')
    browser.close()

with sync_playwright() as playwright:
    run(playwright)