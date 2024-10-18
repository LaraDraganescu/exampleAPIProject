from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Text Box')]").click()

    page.locator('#userName').fill('John')
    page.locator('#userEmail').fill('john@yahoo.com')
    page.locator('#currentAddress').fill('Romania')
    page.locator('#permanentAddress').fill('something')

    page.locator('#submit').click()

    browser.close()
with sync_playwright() as playwright:
    run(playwright)