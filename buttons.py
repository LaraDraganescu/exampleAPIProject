from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Buttons')]").click()


    double_click_text="You have done a double click"
    right_click_text="You have done a right click"
    click_text="You have done a dynamic click"


    page.locator("#doubleClickBtn").dblclick()
    double_button = page.locator('#doubleClickMessage').inner_text()
    if double_button==double_click_text:
        print("message double click")
    else:
        print("message does not appear")

    page.get_by_text("Right Click Me").click(button="right")
    right_button=page.locator('#rightClickMessage').inner_text()
    if right_button==right_click_text:
        print("message right click")
    else:
        print("message does not appear")

    page.get_by_text("Click Me", exact=True).click()
    click_button=page.locator('#dynamicClickMessage').inner_text()
    if click_button==click_text:
        print("message dynamic click")
    else:
        print("message does not appear")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)