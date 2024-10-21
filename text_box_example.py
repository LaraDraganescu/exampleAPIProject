from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Text Box')]").click()

    data={
        "userName": "John",
        "userEmail":"john@yahoo.com",
        "currentAddress":"Romania",
        "permanentAddress":"something"
    }
    page.locator('#userName').fill(data['userName'])
    page.locator('#userEmail').fill(data['userEmail'])
    page.locator('#currentAddress').fill(data['currentAddress'])
    page.locator('#permanentAddress').fill(data['permanentAddress'])

    page.locator('#submit').click()

    name = page.locator('#name').inner_text().replace("Name:", "").strip()
    email = page.locator('#email').inner_text().replace("Email:", "").strip()
    current_address = page.locator('p#currentAddress').inner_text().replace("Current Address :", "").strip()
    permanent_address = page.locator('p#permanentAddress').inner_text().replace("Permananet Address :", "").strip()

    print("match" if name==data['userName'] else "don't match")
    print("match" if email==data['userEmail'] else "don't match")
    print("match" if current_address==data['currentAddress'] else "don't match")
    print("match" if permanent_address==data['permanentAddress'] else "don't match")

    browser.close()
with sync_playwright() as playwright:
    run(playwright)