import time

import pytest
from playwright.sync_api import sync_playwright

class TestExampleClass:

    @pytest.fixture(scope="function")
    def page_demo(self,request):
        elem_page, elem_subpage = request.param
        playwright = sync_playwright().start()
        chromium = playwright.chromium
        browser = chromium.launch()
        page = browser.new_page()
        page.goto("https://demoqa.com")

        page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
        grup_elements = page.locator(
            f"xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), '{elem_page}')] ]"
        )
        grup_elements.locator(f"xpath=.//span[contains(text(), '{elem_subpage}')]").click()


        yield page #returneaza page ca sa fie utilizat in test si revine inapoi pt a face close() (cleanup)

        page.close()
        browser.close()
        playwright.stop()


    # def go_to_element(self, page, elem_page,elem_subpage):
    #     page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
    #     grup_elements = page.locator(
    #         f"xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), '{elem_page}')] ]"
    #     )
    #     grup_elements.locator(f"xpath=.//span[contains(text(), '{elem_subpage}')]").click()

    def expand_checkboxes(self,page, path):
        steps = path.split('>')

        for i, step in enumerate(steps):
            step = step.strip()

            title_locator = page.locator(f"xpath=.//span[@class='rct-title' and text()='{step}']")
            button = title_locator.locator("xpath=../preceding-sibling::button")
            if button.is_visible():
                button.click()

            if i == len(steps) - 1:
                title_locator.click()

    def add_record(self,page, registration_data):
        page.locator('#addNewRecordButton').click()
        page.wait_for_selector("#userForm")
        page.fill("#firstName", registration_data["firstName"])
        page.fill("#lastName", registration_data["lastName"])
        page.fill("#userEmail", registration_data["userEmail"])
        page.fill("#age", registration_data["age"])
        page.fill("#salary", registration_data["salary"])
        page.fill("#department", registration_data["department"])
        page.click("#submit")

    def edit_record(self,page, term, edit_data):
        row = page.locator(
            f"xpath=.//div[@class='rt-tr-group' and .//div[@class='rt-td' and contains(text(), '{term}')]]")
        row.locator("xpath=.//span[@title='Edit']").click()
        page.wait_for_selector("#userForm")

        page.fill("#firstName", edit_data["firstName"])
        page.fill("#lastName", edit_data["lastName"])
        page.fill("#userEmail", edit_data["userEmail"])
        page.fill("#age", edit_data["age"])
        page.fill("#salary", edit_data["salary"])
        page.fill("#department", edit_data["department"])
        page.click("#submit")

    def delete_record(self,page, term):
        row = page.locator(
            f"xpath=.//div[@class='rt-tr-group' and .//div[@class='rt-td' and contains(text(), '{term}')]]")
        row.locator("xpath=.//span[@title='Delete']").click()

    def search(self,page, term):
        page.locator('#searchBox').fill(term)

    def extract_table_data(self,page):
        table_data = []
        rows = page.locator("xpath=.//div[@class='rt-tr-group']")
        row_count = rows.count()

        for row_index in range(row_count):
            row = rows.nth(row_index)
            row_data = {
                "firstName": row.locator("xpath=.//div[@class='rt-td'][1]").inner_text(),
                "lastName": row.locator("xpath=.//div[@class='rt-td'][2]").inner_text(),
                "age": row.locator("xpath=.//div[@class='rt-td'][3]").inner_text(),
                "userEmail": row.locator("xpath=.//div[@class='rt-td'][4]").inner_text(),
                "salary": row.locator("xpath=.//div[@class='rt-td'][5]").inner_text(),
                "department": row.locator("xpath=.//div[@class='rt-td'][6]").inner_text(),
            }
            table_data.append(row_data)

        return table_data

    def verify_row(self,table_data, expected_data):
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

    def check(self,page, data):
        table_data = self.extract_table_data(page)
        self.verify_row(table_data, data)

    def verify_deletion(self,page, field, value):
        table_data = self.extract_table_data(page)
        for row in table_data:
            if row[field] == value:
                return False
        return True

    # @pytest.mark.sanity
    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Radio Button'),
    ], indirect=True) #indirect e necesar ca sa fie tratati ca si parametrii pentru fixture, fara indirect ar astepta params sa fie folositi in fuctia de test
    def test_yes_button(self, page_demo):
        # self.go_to_element(page_demo, 'Elements','Radio Button')
        page_demo.locator('label[for="yesRadio"]').check()
        assert page_demo.is_checked('#yesRadio'), "Yes button was not selected"

    # @pytest.mark.sanity
    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Radio Button'),
    ], indirect=True)
    def test_impressive_button(self, page_demo):
        # self.go_to_element(page_demo, 'Elements', 'Radio Button')
        page_demo.locator('label[for="impressiveRadio"]').check()
        assert page_demo.is_checked('#impressiveRadio'), "Impressive button was not selected"

    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Radio Button'),
    ], indirect=True)
    def test_no_button(self, page_demo):
        # self.go_to_element(page_demo, 'Elements', 'Radio Button')
        assert page_demo.is_disabled('#noRadio'), "'no' button is enabled"

    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Text Box'),
    ], indirect=True)
    def test_text_box(self,page_demo):
        # self.go_to_element(page_demo, 'Elements', 'Text Box')
        data = {
            "userName": "John",
            "userEmail": "john@yahoo.com",
            "currentAddress": "Romania",
            "permanentAddress": "something"
        }
        page_demo.locator('#userName').fill(data['userName'])
        page_demo.locator('#userEmail').fill(data['userEmail'])
        page_demo.locator('#currentAddress').fill(data['currentAddress'])
        page_demo.locator('#permanentAddress').fill(data['permanentAddress'])

        page_demo.locator('#submit').click()

        name = page_demo.locator('#name').inner_text().replace("Name:", "").strip()
        email = page_demo.locator('#email').inner_text().replace("Email:", "").strip()
        current_address = page_demo.locator('p#currentAddress').inner_text().replace("Current Address :", "").strip()
        permanent_address = page_demo.locator('p#permanentAddress').inner_text().replace("Permananet Address :", "").strip()

        assert name == data['userName'], "Name does not match"
        assert email == data['userEmail'], "Email does not match"
        assert current_address == data['currentAddress'], "Current address does not match"
        assert permanent_address == data['permanentAddress'], "Permanent address does not match"

    # @pytest.mark.sanity
    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Check Box'),
    ], indirect=True)
    def test_checkbox(self,page_demo):
        # self.go_to_element(page_demo,"Elements", "Check Box")
        self.expand_checkboxes(page_demo, "Home > Documents>Office")
        expected_selections = ["office", "public", "private", "classified", "general"]

        selected = page_demo.locator("xpath=.//span[@class='text-success']").all_inner_texts()
        assert expected_selections == selected, "not match"

    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Buttons'),
    ], indirect=True)
    def test_buttons(self,page_demo):
        # self.go_to_element(page_demo, "Elements", "Buttons")
        double_click_text = "You have done a double click"
        right_click_text = "You have done a right click"
        click_text = "You have done a dynamic click"

        page_demo.locator("#doubleClickBtn").dblclick()
        double_button = page_demo.locator('#doubleClickMessage').inner_text()
        assert double_button == double_click_text, "Double click message does not match"

        page_demo.get_by_text("Right Click Me").click(button="right")
        right_button = page_demo.locator('#rightClickMessage').inner_text()
        assert right_button == right_click_text, "Right click message does not match"

        page_demo.get_by_text("Click Me", exact=True).click()
        click_button = page_demo.locator('#dynamicClickMessage').inner_text()
        assert click_button == click_text, "Dynamic click message does not match"

    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Dynamic Properties'),
    ], indirect=True)
    def test_dynamic(self,page_demo):
        # self.go_to_element(page_demo, "Elements", "Dynamic Properties")

        disable_button = page_demo.is_disabled('#enableAfter')
        assert disable_button, "Button is not disabled"

        color_button = page_demo.locator('#colorChange')
        class_button = color_button.get_attribute("class")
        assert "text-danger" not in class_button, "'text-danger' not found in button"

        time.sleep(5)

        is_enable = page_demo.is_enabled('#enableAfter')
        assert is_enable, "Button is not enabled"

        visible = page_demo.is_visible('#visibleAfter')
        assert visible, "Button is not visible"
        changed_class = color_button.get_attribute("class")
        assert "text-danger" in changed_class, "'text-danger' not found after change"

    @pytest.mark.parametrize("page_demo", [
        ('Elements', 'Web Tables'),
    ], indirect=True)
    def test_web_tables(self,page_demo):
        # self.go_to_element(page_demo, "Elements", "Web Tables")
        registration_data = {
            "firstName": "John",
            "lastName": "Doe",
            "userEmail": "john_doe@example.com",
            "age": "49",
            "salary": "12000",
            "department": "IT"
        }

        self.add_record(page_demo, registration_data)
        assert self.verify_row(self.extract_table_data(page_demo), registration_data), "Record not found after adding"

        edit_data = {
            "firstName": "New Cierra",
            "lastName": "New Vega",
            "userEmail": "noua_cierra@example.com",
            "age": "40",
            "salary": "12000",
            "department": "New Insurance"
        }

        self.edit_record(page_demo, "Vega", edit_data)
        assert self.verify_row(self.extract_table_data(page_demo), edit_data), "Record not found after editing"

        self.delete_record(page_demo, "noua_cierra@example.com")
        assert self.verify_deletion(page_demo, "userEmail", "noua_cierra@example.com"), "Record still exists after deletion"

        self.search(page_demo, "it")
        table_data = self.extract_table_data(page_demo)
        if table_data:
            first_row = table_data[0]
            assert self.verify_row([first_row], registration_data), "Search result does not match expected data"



# def run(playwright: Playwright):
#     chromium = playwright.chromium # or "firefox" or "webkit".
#     browser = chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://demoqa.com")
#
#     page.locator("xpath=//h5[contains(text(), 'Elements')]").click()
#     grup_elements=page.locator("xpath=.//div[@class='element-group' and .//div[@class='header-text' and contains(text(), 'Elements')] ]")
#     grup_elements.locator("xpath=.//span[contains(text(), 'Radio Button')]").click()
#
#     page.locator('label[for="impressiveRadio"]').check()
#     page.locator('label[for="yesRadio"]').check()
#
#     yes_button=page.is_checked('#yesRadio')
#     impressive = page.is_checked('#impressiveRadio')
#     if yes_button:
#         print("yes was selected")
#     elif impressive:
#         print("'impressive was selected'")
#     else:
#         print("nothing was selected")
#
#
#     no_button = page.is_disabled("#noRadio")
#     if no_button:
#         print("disabled")
#     else:
#         print("enabled")
#
#     browser.close()
#
#
#
# with sync_playwright() as playwright:
#     run(playwright)