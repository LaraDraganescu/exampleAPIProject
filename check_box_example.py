from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elements=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')] ]")
    grup_elements.locator("xpath=.//span[contains(text(), 'Check Box')]").click()

    # page.locator("xpath=.//span[@class='rct-checkbox']").click()


    page.get_by_role("button", name="Expand all").click()
    # home = page.get_by_role("button", name="Toggle")
    # home.click()

    page.locator("label[for='tree-node-react']").check()

    # page.get_by_role("button",name="Toggle").click()


    # page.get_by_label("tree-node-desktop").click()

    # page.locator("xpath=.//*[@class='rct-title' and contains(text(), 'Home']]").check()
    # page.locator("xpath=.//span[@class='rct-checkbox' and .//span[@class='rct-title' and contains(text(), 'Private')]]").click()

    # page.locator("xpath=//*[@id='tree-node-home']").click()



    browser.close()


with sync_playwright() as playwright:
    run(playwright)