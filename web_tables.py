from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Web Tables')]").click()

    page.locator("xpath=.//*[@id='edit-record-1']").click()
    page.wait_for_selector("#userForm")
    page.fill("#firstName", "Noua Cierra")
    page.fill("#lastName", "Noua Vega")
    page.fill("#userEmail", "noua_cierra@example.com")
    page.fill("#age", "40")
    page.fill("#salary", "12000")
    page.fill("#department", "Noua Insurance")

    page.click("#submit")

    page.locator("xpath=.//*[@id='delete-record-2']").click()

    page.locator('#addNewRecordButton').click()
    page.wait_for_selector("#userForm")
    page.fill("#firstName", "registration")
    page.fill("#lastName", "last name")
    page.fill("#userEmail", "noua_cierra@example.com")
    page.fill("#age", "40")
    page.fill("#salary", "12000")
    page.fill("#department", "Noua Insurance")
    page.click("#submit")

    browser.close()


with sync_playwright() as playwright:
    run(playwright)