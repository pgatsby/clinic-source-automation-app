import traceback
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import os
import time

from dotenv import load_dotenv
load_dotenv()


# Set up logging
logging.basicConfig(filename='error_log.log', level=logging.ERROR)

# Global variable to hold the socketio instance
socketio = None

# Environment variable for WebDriverWait timeout
TIMEOUT = int(os.getenv('WAIT_TIMEOUT', '15'))  # Default to 15 if not set


def set_socketio_instance(sio):
    try:
        global socketio
        socketio = sio
    except Exception as e:
        add_log(f"An error occurred: {traceback.format_exc()}")
        logging.error(
            f"Set SocketIO Instance Failed: {traceback.format_exc()}")


def add_log(message):
    if "successfully" in message.lower():
        message = f"✓ {message}"
    elif "error" in message.lower() or "exception" in message.lower():
        message = f"x {message}"
    else:
        message = f"— {message}"

    print(message)
    # Emit the log message using the socketio instance
    if socketio:
        socketio.emit('log_message', {'data': message})


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")


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
    add_log("Driver Setup Successfully")

    return driver


def login(clinic_name, username, password):
    driver = setup_driver()
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
        add_log("Logged In Successfully")
        return driver
    except Exception as e:
        add_log(
            f"Wrong Credentials, Double Check Clinic Name or Username or Password: {traceback.format_exc()}")
        logging.error(f"Login Failed: {traceback.format_exc()}")
        driver.quit()  # Close the driver
        return False


def navigate_to_visits_page(driver):
    try:
        # Navigate to the next page
        driver.get("https://app.clinicsource.com/ClinicPortal/Visits.aspx")

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.ID, 'lbPatients_i0')
            )
        )
        add_log("Navigated to PT Visits Page Successfully")
    except Exception as e:
        add_log(f"An error occurred: {traceback.format_exc()}")
        logging.error(
            f"Navigation to Visit Page Failed: {traceback.format_exc()}")
        driver.quit()  # Close the driver
        return False


def autofill_pt_info(clinic_name, username, password, num_of_pts):
    try:
        driver = login(clinic_name, username, password)

        if not driver:
            return False

        navigate_to_visits_page(driver)

        all_input = driver.find_element(By.ID, 'lbPatients_i0')
        all_input.click()

        WebDriverWait(driver, TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dgVisits_ctl00"))
        )

        add_log("Access PTs Table Successfully")

        for index in range(num_of_pts):
            WebDriverWait(driver, TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//*[starts-with(@id, 'dgVisits_ctl00__')]"))
            )

            add_log("Access PT Row Successfully")

            # Reacquire the table and rows on each iteration to avoid stale references
            pt_table = driver.find_element(By.ID, "dgVisits_ctl00")
            # Find all elements where the ID starts with 'dgVisits_ctl00__'
            pt_rows = pt_table.find_elements(
                By.XPATH, "//*[starts-with(@id, 'dgVisits_ctl00__')]")

            pt_row = pt_rows[index]

            try:
                # Try to find the td containing the specific img
                img = pt_row.find_element(
                    By.XPATH, ".//td/img[@src='images/checkmark.gif']")
            except:
                pt_row.click()

                WebDriverWait(driver, TIMEOUT).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//*[contains(@id, 'PageToolbar_') and contains(@id, '_btnInsert')]"))
                )
                add_log("Navigated to PT Page Successfully")

                template_insert_button = driver.find_element(
                    By.XPATH, "//*[contains(@id, 'PageToolbar_') and contains(@id, '_btnInsert')]")
                template_insert_button.click()

                # Wait for page to load
                # WebDriverWait(driver, TIMEOUT).until(
                #     expected_conditions.presence_of_element_located(
                #         (By.XPATH, "//a[@title='Edit Template']"))
                # )

                # edit_template_button = driver.find_element(
                #     By.XPATH, "//a[@title='Edit Template']")

                # edit_template_button.click()

                WebDriverWait(driver, TIMEOUT).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//table[contains(@id, 'CustomTemplate_') and contains(@id, '_C_TemplateItem_') and contains(@id, '_tblGoals')]"))
                )

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
                                f"An error occurred: {traceback.format_exc()}")
                            logging.error(
                                f"Autofill - Setting Goals Failed: {traceback.format_exc()}")

                add_log("Updated PT Goals Successfully")

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
                        add_log(f"An error occurred: {traceback.format_exc()}")
                        logging.error(
                            f"Autofill - Setting Previous Comment Failed: {traceback.format_exc()}")

                save_button = driver.find_element(
                    By.XPATH, "//a[@title='Save Changes']")

                save_button.click()
                add_log("Saved Patient Info Successfully")

                # After processing, navigate back to the original page
                driver.get(
                    "https://app.clinicsource.com/ClinicPortal/Visits.aspx")
                # Waits for the visits page to load
                WebDriverWait(driver, TIMEOUT).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "Header_PageMenu_i16_lbUserName"))
                )

            add_log(f"Completed: {index + 1}/{num_of_pts}")

         # Calculate progress percentage
            progress_percentage = ((index + 1) / num_of_pts) * 100

            # Emit an event with the progress
            if socketio:
                socketio.emit('task_completed', {
                              'completedPercentage': progress_percentage})
                # Close the browser
        driver.close()

        return True
    except Exception as e:
        add_log(f"An error occurred: {traceback.format_exc()}")
        logging.error(f"Autofill Failed: {traceback.format_exc()}")
        return False


def run(clinic_name, username, password, num_of_pts):

    return autofill_pt_info(clinic_name, username, password, int(num_of_pts))
