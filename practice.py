from playwright.sync_api import sync_playwright, Playwright


def fill_form(page, data):
    labels=page.locator("xpath=.//div[@class='mt-2 row']").all_inner_texts()

    for label in labels:
        if 'Name' in label:
            page.locator("#firstName").fill(data['Name'][0])
            page.locator("#lastName").fill(data['Name'][1])

            first_entered = page.locator("#firstName").input_value()
            last_entered = page.locator("#lastName").input_value()
            if first_entered == data['Name'][0]:
                print("first name corect")
            else:
                print("first name not correct")

            if last_entered == data['Name'][1]:
                print("last name corect")
            else:
                print("last name not correct")

        if 'Email' in label:
            page.locator("#userEmail").fill(data['Email'])

            email_entered = page.locator("#userEmail").input_value()
            if email_entered == data['Email']:
                print("email corect")
            else:
                print("email not correct")
        if 'Gender' in label:
            gender=data["Gender"]
            gender_radio=page.locator(f"xpath=.//label[text()='{gender}']")
            gender_radio.click()

            if gender_radio.is_checked():
                print("is checked")
            else:
                print("not checked")

        if 'Mobile' in label:
            page.locator("#userNumber").fill(data['Mobile'])

            mobile_entered = page.locator("#userNumber").input_value()
            if mobile_entered==data['Mobile']:
                print("mobile corect")
            else:
                print("mobile not correct")
        if 'Birth' in label:
            page.locator("#dateOfBirthInput").fill(data['DateofBirth'])
            page.locator("#dateOfBirthInput").press("Enter")
        if 'Subjects' in label:
            for sub in data['Subjects']:
                page.locator("#subjectsInput").fill(sub)
                page.locator("#subjectsInput").press("Enter")

                subj_filled=page.locator("xpath=.//div[@class='css-1rhbuit-multiValue subjects-auto-complete__multi-value']").all_inner_texts()
                if sub in subj_filled:
                    print("subject added")
                else:
                    print("not added")
            # page.locator(f"xpath=.//div[contains(text(), '{subject}')]").click()

        if 'Picture' in label:
            picture=data['Picture']
            with page.expect_file_chooser() as fc_info:
                page.get_by_text("Select picture").click()
            file_chooser = fc_info.value
            file_chooser.set_files(picture)
        if 'Hobbies' in label:
           for hobby in data['Hobbies']:
                hobby_check=page.locator(f"xpath=.//label[text()='{hobby}']")
                hobby_check.check()

                if hobby_check.is_checked():
                    print("hobby button checked")
                else:
                    print("hobby button not checked")

        if 'Address' in label:
            page.locator("#currentAddress").fill(data['CurrentAddress'])

            address_entered=page.locator("#currentAddress").input_value()
            if address_entered==data['CurrentAddress']:
                print("address corect")
            else:
                print("address not correct")

        if 'State' in label:
            state=data["StateandCity"][0]
            city=data["StateandCity"][1]

            city_button= page.locator("xpath=.//div[text()='Select City']")
            if city_button.is_disabled():
                print("disabled before selecting state")
            else:
                print("is not disabled before selecting state")

            page.locator("xpath=.//div[text()='Select State']").click()
            page.locator(f"xpath=.//div[contains(text(), '{state}')]").click()

            if city_button.is_enabled():
                print("enblaed after selecting state")
            else:
                print("not enbaled after selcting state")

            city_button.click()
            page.locator(f"xpath=.//div[contains(text(), '{city}')]").click()

    page.wait_for_timeout(5000)
    page.locator("#submit").click()



def extract_table_data(page):
    extracted_data = {}

    rows = page.locator("//table/tbody/tr")
    row_count = rows.count()

    for row_index in range(row_count):
        row = rows.nth(row_index)
        label = row.locator("td").nth(0).inner_text().strip()
        value = row.locator("td").nth(1).inner_text().strip()
        extracted_data[label] = value

    return extracted_data



def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com")

    page.locator("xpath=.//h5[contains(text(),'Forms')]").click()
    page.locator("xpath=.//span[contains(text(),'Practice Form')]").click()


    data={
        "Name":["John", "Doe"],
        "Email":"johndoe@yahoo.com",
        "Gender":"Other",
        "Mobile":"1234567899",
        "DateofBirth":"10 Oct 1998",
        "Subjects":["Physics","English"],
        "Picture":"/Users/ldragane/Desktop/pic.png",
        "Hobbies":["Music","Sports"],
        "CurrentAddress":"US",
        "StateandCity":["NCR","Delhi"]
    }

    fill_form(page,data)
    page.wait_for_selector(".modal-content", timeout=5000)
    table_data=extract_table_data(page)

    expected_data= {
        "Student Name": " ".join(data["Name"]),
        "Student Email": data["Email"],
        "Gender": data["Gender"],
        "Mobile": data["Mobile"],
        "Date of Birth": data["DateofBirth"],
        "Subjects": ", ".join(data["Subjects"]),
        "Hobbies": ", ".join(data["Hobbies"]),
        "Address": data["CurrentAddress"],
        "State and City": " ".join(data["StateandCity"])
    }

    if table_data==expected_data:
        print("identical")
    else:
        print("not")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)