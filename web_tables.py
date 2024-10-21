from playwright.sync_api import sync_playwright, Playwright

def add_record(page, registration_data):
    page.locator('#addNewRecordButton').click()
    page.wait_for_selector("#userForm")
    page.fill("#firstName", registration_data["firstName"])
    page.fill("#lastName", registration_data["lastName"])
    page.fill("#userEmail", registration_data["userEmail"])
    page.fill("#age", registration_data["age"])
    page.fill("#salary", registration_data["salary"])
    page.fill("#department", registration_data["department"])
    page.click("#submit")


def edit_record(page, term, edit_data):
    row = page.locator(f"xpath=.//div[@class='rt-tr-group' and .//div[@class='rt-td' and contains(text(), '{term}')]]")
    row.locator("xpath=.//span[@title='Edit']").click()
    page.wait_for_selector("#userForm")

    page.fill("#firstName", edit_data["firstName"])
    page.fill("#lastName", edit_data["lastName"])
    page.fill("#userEmail", edit_data["userEmail"])
    page.fill("#age", edit_data["age"])
    page.fill("#salary", edit_data["salary"])
    page.fill("#department", edit_data["department"])
    page.click("#submit")

def delete_record(page, term):
    row = page.locator(f"xpath=.//div[@class='rt-tr-group' and .//div[@class='rt-td' and contains(text(), '{term}')]]")
    row.locator("xpath=.//span[@title='Delete']").click()

def search(page, term):
    page.locator('#searchBox').fill(term)

def extract_table_data(page):
    table_data = []
    row_count = page.locator(".rt-tr-group").count()

    for row_index in range(1, row_count + 1):
        row = page.locator(f".rt-tr-group:nth-child({row_index})")

        row_data = {
            "firstName": row.locator(".rt-td:nth-child(1)").inner_text(),
            "lastName": row.locator(".rt-td:nth-child(2)").inner_text(),
            "age": row.locator(".rt-td:nth-child(3)").inner_text(),
            "userEmail": row.locator(".rt-td:nth-child(4)").inner_text(),
            "salary": row.locator(".rt-td:nth-child(5)").inner_text(),
            "department": row.locator(".rt-td:nth-child(6)").inner_text(),
        }

        table_data.append(row_data)

    return table_data


def verify_row(table_data, expected_data):
    for row in table_data:
        if (row["firstName"] == expected_data["firstName"] and
            row["lastName"] == expected_data["lastName"] and
            row["age"] == expected_data["age"] and
            row["userEmail"] == expected_data["userEmail"] and
            row["salary"] == expected_data["salary"] and
            row["department"] == expected_data["department"]):
            print("found:", row)
            return True
    print("not found:", expected_data)
    return False


# def verify_row(page, row_index, expected_data):
#     row = page.locator(f"xpath=.//div[@class='rt-tr-group'][{row_index}]")
#     changed_name = row.locator("xpath=.//div[@class='rt-td'][1]").inner_text()
#     changed_last = row.locator("xpath=.//div[@class='rt-td'][2]").inner_text()
#     changed_age = row.locator("xpath=.//div[@class='rt-td'][3]").inner_text()
#     changed_email = row.locator("xpath=.//div[@class='rt-td'][4]").inner_text()
#     changed_salary = row.locator("xpath=.//div[@class='rt-td'][5]").inner_text()
#     changed_department = row.locator("xpath=.//div[@class='rt-td'][6]").inner_text()
#
#     print("match" if changed_name == expected_data["firstName"] else "don't match")
#     print("match" if changed_last == expected_data["lastName"] else "don't match")
#     print("match" if changed_age == expected_data["age"] else "don't match")
#     print("match" if changed_email == expected_data["userEmail"] else "don't match")
#     print("match" if changed_salary == expected_data["salary"] else "don't match")
#     print("match" if changed_department == expected_data["department"] else "don't match")


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    grup_elemente=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')]]")
    grup_elemente.locator("xpath=.//span[contains(text(),'Web Tables')]").click()


    # tabel= extract_table_data(page)
    # print(tabel)

    registration_data = {
        "firstName": "John",
        "lastName": "Doe",
        "userEmail": "john_doe@example.com",
        "age": "49",
        "salary": "12000",
        "department": "IT"
    }

    add_record(page, registration_data)
    table_data = extract_table_data(page)
    verify_row(table_data,registration_data)


    edit_data = {
        "firstName": "New Cierra",
        "lastName": "New Vega",
        "userEmail": "noua_cierra@example.com",
        "age": "40",
        "salary": "12000",
        "department": "New Insurance"
    }

    edit_record(page, "Vega", edit_data)
    table_data2 = extract_table_data(page)
    verify_row(table_data2, edit_data)


    delete_record(page, "kierra@example.com")
    tabel_data6=extract_table_data(page)
    # verify_row(tabel_data6, edit_data)

    search(page, "it")
    tabel_data4=extract_table_data(page)
    if tabel_data4:
        first_row = tabel_data4[0]
        verify_row([first_row],registration_data)

    browser.close()


with sync_playwright() as playwright:
    run(playwright)