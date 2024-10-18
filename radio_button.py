from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elements=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')] ]")
    grup_elements.locator("xpath=.//span[contains(text(), 'Radio Button')]").click()

    # page.get_by_label('Impressive').check()
    # page.get_by_label('impressiveRadio').check()

    # page.check(".//input[@id='yesRadio']")
    # page.locator("#yesRadio").click()


    page.locator('label[for="impressiveRadio"]').check()
    no_button = page.is_disabled("#noRadio")
    if no_button:
        print("disabled")
    else:
        print("enabled")

    browser.close()



with sync_playwright() as playwright:
    run(playwright)