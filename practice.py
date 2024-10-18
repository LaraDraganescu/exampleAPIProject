from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=.//h5[contains(text(),'Forms')]").click()
    page.locator("xpath=.//span[contains(text(),'Practice Form')]").click()

    page.locator('#firstName').fill("John")
    page.locator('#lastName').fill("Doe")
    page.locator('#userEmail').fill("john.doe@ai.com")

    page.locator('label[for="gender-radio-1"]').click()
    # page.locator('xpath=//*[@id="dateOfBirthInput"]')
    # page.locator('xpath=.//*[@id="hobbies-checkbox-1]').click()
    page.locator('label[for="hobbies-checkbox-2"]').click()
    page.locator('#currentAddress').fill("text text")
    page.locator('#submit').click()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)