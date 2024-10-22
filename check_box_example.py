from playwright.sync_api import sync_playwright, Playwright
from select import select


def expand_checkboxes(page, path):
    steps = path.split('>')

    for i, step in enumerate(steps):
        step = step.strip()

        title_locator = page.locator(f"xpath=.//span[@class='rct-title' and text()='{step}']")
        button=title_locator.locator("xpath=../preceding-sibling::button")
        if button.is_visible():
            button.click()

        if i==len(steps)-1:
            title_locator.click()

        # check=page.locator(f"xpath=.//span[contains(text(), '{step}')]")
        # page.locator("xpath=.//button[@title='Toggle']").click()

        # checkbox = page.locator(f"xpath=.//span[@class='rct-title' and contains(text(), '{step}')]").highlight()
        # toggle_button = checkbox.locator("xpath=.//span[@class='rct-title' and .//button[@title='Toggle']]").highlight()
        # toggle_button.click()


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elements=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')] ]")
    grup_elements.locator("xpath=.//span[contains(text(), 'Check Box')]").click()

    expand_checkboxes(page, "Home > Documents>Office")
    expected_selections = ["office", "public", "private", "classified", "general"]


    selected=page.locator("xpath=.//span[@class='text-success']").all_inner_texts()
    if selected==expected_selections:
        print("similar")
    else:
        print("not similar")

    browser.close()


with sync_playwright() as playwright:
    run(playwright)