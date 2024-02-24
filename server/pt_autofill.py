from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from http import HTTPStatus

import os
import time

from dotenv import load_dotenv
load_dotenv()

# Global variable to hold the socketio instance
socketio = None

# Global variable for driver
driver = None

# Environment variable for debug
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# Environment variable for WebDriverWait timeout
TIMEOUT = int(os.environ.get('WAIT_TIMEOUT', '10'))  # Default to 10 if not set


def set_socketio_instance(sio):
    try:
        global socketio
        socketio = sio
    except Exception as e:
        add_log(f"Socket Connection Failed: {HTTPStatus.BAD_REQUEST.value}")


def add_log(message):
    if str(HTTPStatus.OK.value) in message:
        message = f"✓ {message}"
    elif str(HTTPStatus.BAD_REQUEST.value) in message:
        message = f"x {message}"
    else:
        message = f"— {message}"

    print(message)
    # Emit the log message using the socketio instance
    if socketio:
        socketio.emit('log_message', {'data': message})


def setup_driver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")

    if not DEBUG:

        # Use environment variables set by the buildpacks
        chrome_binary = os.environ.get("GOOGLE_CHROME_BIN")
        if chrome_binary:
            chrome_options.binary_location = chrome_binary

        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", "chromedriver")
        service = Service(executable_path=chromedriver_path)

        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the website
        driver.get("https://app.clinicsource.com/")

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "TableLogin")
            )
        )
        add_log(f"Driver Setup: {HTTPStatus.OK.value}")

    else:
        # Debugging on localhost
        chrome_options = Options()

        driver = webdriver.Chrome(options=chrome_options)

        # Go to the website
        driver.get("https://app.clinicsource.com/")

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "TableLogin")
            )
        )
        add_log(f"Driver Setup: {HTTPStatus.OK.value}")


def login(clinic_name, username, password):
    setup_driver()

    # Find the form elements and try to login
    try:
        # Find the form elements
        clinic_name_input = driver.find_element(By.ID, "tbClinicName")
        username_input = driver.find_element(By.ID, "txtUsr")
        password_input = driver.find_element(By.ID, "txtPwd")

        login_button = driver.find_element(By.ID, "Button1")

        # Fill out the form
        clinic_name_input.send_keys(clinic_name)
        username_input.send_keys(username)
        password_input.send_keys(password)

        # Click the submit button
        login_button.click()

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "Header_PageMenu_i16_lbUserName"))
        )
        add_log(f"Login Request Success: {HTTPStatus.OK.value}")
        return True
    except Exception as e:
        add_log(
            f"Login Request Failed: {HTTPStatus.BAD_REQUEST.value}")
        return False


def navigate_to_visits_page():

    try:
        # Navigate to the next page
        driver.get("https://app.clinicsource.com/ClinicPortal/Visits.aspx")

        # time.sleep(TIMEOUT)

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.ID, 'lbPatients_i0')
            )
        )
        add_log(f"PT Visits Request: {HTTPStatus.OK.value}")
    except Exception as e:
        add_log(f"PT Visits Request Failed: {HTTPStatus.BAD_REQUEST.value}")


def get_pt_names():

    try:

        navigate_to_visits_page()

        # Extract patient names
        patient_names = [element.text.strip()
                         for element in driver.find_elements(By.CLASS_NAME, 'rlbText')]

        add_log(f"Fetched Patient Names: {HTTPStatus.OK.value}")

        return patient_names

    except Exception as e:
        add_log(
            f"Fetched Patient Names Failed: {HTTPStatus.BAD_REQUEST.value}")
        return []


def get_pt_rows_without_notes():

    try:

        pt_table = driver.find_element(By.ID, "dgVisits_ctl00")
        pt_rows = pt_table.find_elements(
            By.XPATH, "//*[starts-with(@id, 'dgVisits_ctl00__')]")

        if not pt_rows:
            add_log("No patient rows found.")
            return []

        # Filter out rows that contain the specified image
        pt_rows_without_notes = [row for row in pt_rows if not row.find_elements(
            By.XPATH, ".//img[@src='images/checkmark.gif']")]

        return pt_rows_without_notes
    except Exception as e:
        add_log(
            f"Fetched Patient Rows without Notes Failed: {HTTPStatus.BAD_REQUEST.value}")
        return []


def autofill_pt_goals():

    goals_table = driver.find_element(
        By.XPATH, "//table[contains(@id, 'CustomTemplate_') and contains(@id, '_C_TemplateItem_') and contains(@id, '_tblGoals')]")

    goal_rows = goals_table.find_elements(By.TAG_NAME, "tr")

    for goal_row in goal_rows:
        # Get the 5th, 6th, and 7th td elements
        td_elements = goal_row.find_elements(
            By.XPATH, ".//td[position()=5 or position()=6 or position()=7]")

        for td in td_elements[3::]:
            try:
                # Find the select element inside the nested table structure
                select_element = td.find_element(
                    By.XPATH, ".//table//select")
                last_value_span = td.find_element(
                    By.XPATH, ".//div[@class='SmallGrayComment']/span")

                # Extract the text from the span
                full_text = last_value_span.text.strip()

                # Check if the text starts with 'Last: '
                if full_text.startswith("Last: "):
                    # Extract the value after 'Last: '
                    last_value = full_text.split()[-1]
                else:
                    # Use the full text if it doesn't start with 'Last: '
                    last_value = full_text

                # Now continue with your checks and logic
                if not last_value or last_value.lower() == 'none':
                    continue

                 # Iterate through the options and select the matching one
                for option in select_element.find_elements(By.TAG_NAME, "option"):
                    if option.text.strip().lower() == last_value.lower():
                        option.click()
                        break

            except Exception as e:
                add_log(
                    f"Update PT Goals Failed: {HTTPStatus.BAD_REQUEST.value}")

    add_log(f"Update PT Goals: {HTTPStatus.OK.value}")


def autofill_pt_soap():

    # Get the number of copy links initially
    num_of_copy_links = len(driver.find_elements(
        By.XPATH, "//a[@title='Copy From Previous Document']"))

    for i in range(num_of_copy_links):
        # Re-find the copy links on each iteration
        copy_links = driver.find_elements(
            By.XPATH, "//a[@title='Copy From Previous Document']")
        try:
            # Click the i-th link in the list
            copy_links[i].click()

            time.sleep(TIMEOUT)

            # Wait for the dynamic button to appear on the form
            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//input[contains(@id, 'winPrevious_C_btnOkCopy_input')]"))
            )

            # Click the dynamic button
            insert_button = driver.find_element(
                By.XPATH, "//input[contains(@id, 'winPrevious_C_btnOkCopy_input')]")
            insert_button.click()

            time.sleep(TIMEOUT)

            # Update this with the actual XPath of the loading element
            loading_element_xpath = "//div[@class='loading']"
            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.invisibility_of_element_located(
                    (By.XPATH, loading_element_xpath))
            )

        except Exception as e:
            add_log(f"Update PT SOAP Failed: {HTTPStatus.BAD_REQUEST.value}")


def save_pt_info():

    try:
        save_button = driver.find_element(
            By.XPATH, "//a[@title='Save Changes']")

        save_button.click()
        add_log(f"Saved Patient Info: {HTTPStatus.OK.value}")
    except Exception as e:
        add_log(f"Saved Patient Info Failed: {HTTPStatus.BAD_REQUEST.value}")


def autofill_pt_info(pt_name, num_of_notes):

    try:
        if not driver:
            return False

        navigate_to_visits_page()

        if not pt_name:
            all_input = driver.find_element(By.ID, 'lbPatients_i0')
            all_input.click()

            time.sleep(TIMEOUT)

            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "dgVisits_ctl00"))
            )

            add_log(f"Access PTs Table: {HTTPStatus.OK.value}")

        else:
            filter_input = driver.find_element(By.ID, 'filterBox')
            filter_input.send_keys(pt_name)

            time.sleep(TIMEOUT)

            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, f"//li[contains(., '{pt_name}') and contains(@class, 'rlbItem')]"))
            )

            matching_name = driver.find_element(
                By.XPATH, f"//li[contains(., '{pt_name}') and contains(@class, 'rlbItem')]")
            matching_name.click()

            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "dgVisits"))
            )

            add_log(f"Access {pt_name} Table: {HTTPStatus.OK.value}")

        notes_completed = 0

        while notes_completed < num_of_notes:

            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//*[starts-with(@id, 'dgVisits_ctl00__')]"))
            )

            # Fetch patient rows without notes
            pt_rows_without_notes = get_pt_rows_without_notes()

            if not pt_rows_without_notes:
                add_log("No more patients to process or limit reached.")
                break

            # Assume we process the first row for simplicity; adjust as needed
            pt_row = pt_rows_without_notes[0]

            # Example: Clicking on the patient row to open details
            pt_row.click()

            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//*[contains(@id, 'PageToolbar_') and contains(@id, '_btnInsert')]"))
            )
            add_log(f"Navigated to PT Page: {HTTPStatus.OK.value}")

            template_insert_button = driver.find_element(
                By.XPATH, "//*[contains(@id, 'PageToolbar_') and contains(@id, '_btnInsert')]")
            template_insert_button.click()

            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//table[contains(@id, 'CustomTemplate_') and contains(@id, '_C_TemplateItem_') and contains(@id, '_tblGoals')]"))
            )

            autofill_pt_goals()
            autofill_pt_soap()
            save_pt_info()

            notes_completed += 1
            add_log(
                f"Completed {notes_completed}/{num_of_notes}: {HTTPStatus.OK.value}")

            progress_percentage = (notes_completed / num_of_notes) * 100
            if socketio:
                socketio.emit('task_completed', {
                              'completedPercentage': progress_percentage})

            # Return to the visits page to refresh references for the next iteration
            navigate_to_visits_page()

        return True

    except Exception as e:
        add_log(f"Autofill PT Info Failed: {HTTPStatus.BAD_REQUEST.value}")
        return False


def run(num_of_notes, pt_name):
    # Convert the string "None" to None
    if pt_name == "None":
        pt_name = None
    return autofill_pt_info(pt_name, int(num_of_notes))
