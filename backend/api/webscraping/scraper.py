import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from config import USERNAME, PASSWORD, LOGIN_URL, BASE_URL, CHROME_DRIVER_PATH, LOG_FILE
import threading

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--enable-javascript")
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def wait_for_2fa_code(timeout=120, poll_interval=2):
    """Wait for the 2FA code to be written to the file."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Attempt to read the file
            with open("2FAcode.txt", "r") as f:
                code = f.read().strip()
            if code:  # If code is not empty
                return code
        except FileNotFoundError:
            pass  # File might not exist initially

        print("Waiting for 2FA code...")
        time.sleep(poll_interval)  # Wait before checking again

    raise TimeoutError("Timeout waiting for 2FA code.")

def login(driver):
    """Log in to the MyChart portal and handle 2FA."""
    driver.get(LOGIN_URL)
    logging.info("Opening login page...")

    try:
        # Wait for the username field to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "Login"))
        )
        print("Username field located.")

        driver.find_element(By.ID, "Login").send_keys(USERNAME)
        driver.find_element(By.ID, "Password").send_keys(PASSWORD)
        print("Credentials entered.")

        driver.find_element(By.ID, "submit").click()
        logging.info("Sign in button clicked.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "twofactorcode"))
        )
        print("2FA input field located.")

        print("Waiting for 2FA code...")
        try:
            # Wait for the code to appear in the file
            code = wait_for_2fa_code(timeout=120)  # Adjust timeout as needed
        except TimeoutError as e:
            logging.error(str(e))
            raise

        driver.find_element(By.ID, "twofactorcode").send_keys(code)
        print("2FA code entered.")

        driver.find_element(By.ID, "submitSecondaryValidation").click()
        logging.info("2FA code submitted.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Test Results"))  # Element exclusive to homepage
        )
        print("Successfully logged in!")

        with open("2FAcode.txt", "w") as f:
            f.write("")
        print("2FA code file wiped successfully.")

    except Exception as e:
        logging.error(f"Error during login or 2FA: {e}")
        raise

def navigate_and_scrape_visits(driver, output_file):
    """
    Navigate to the Visits page, click all 'View Notes' buttons, scrape text from each directed page,
    and save the data to a fresh JSON file.
    """
    try:
        # Overwrite the file to clear existing data
        with open(output_file, "w") as f:
            json.dump([], f, indent=4)  # Start with an empty JSON array
        print(f"{output_file} has been cleared for a fresh scrape.")

        # Navigate to the Visits page
        visits_url = "https://mychart.uwhealth.org/MyChart/Visits"
        driver.get(visits_url)
        print("Navigated to Visits page.")
        logging.info("Navigated to Visits page.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'notes button')]"))
        )
        print("Page loaded. Checking for 'View Notes' buttons...")

        # Find all "View Notes" buttons
        view_notes_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'notes button')]")
        print(f"Found {len(view_notes_buttons)} 'View Notes' buttons.")

        if not view_notes_buttons:
            print("No 'View Notes' buttons found.")
            logging.info("No 'View Notes' buttons found.")
            return

        # Iterate over each "View Notes" button
        for i, button in enumerate(view_notes_buttons):
            try:
                # Re-fetch buttons each time to avoid stale element exceptions
                view_notes_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'notes button')]")
                button = view_notes_buttons[i]

                print(f"Clicking 'View Notes' button {i + 1}...")
                button.click()
                logging.info(f"Clicked 'View Notes' button {i + 1}.")

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print(f"Notes page {i + 1} loaded.")

                # Scrape the notes page content
                soup = BeautifulSoup(driver.page_source, "html.parser")
                data = soup.get_text()

                # Add the new data as a dictionary
                new_entry = {"content": data}

                # Load the current file content and append new entry
                with open(output_file, "r+") as f:
                    existing_data = json.load(f)
                    existing_data.append(new_entry)
                    # Overwrite the file with updated data
                    f.seek(0)
                    json.dump(existing_data, f, indent=4)

                print(f"Added notes for button {i + 1} to {output_file}.")

                # Go back to the Visits page
                driver.back()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'notes button')]"))
                )
                print("Returned to Visits page.")

            except Exception as e:
                logging.error(f"Error scraping notes for button {i + 1}: {e}")
                print(f"Error scraping notes for button {i + 1}: {e}")

        logging.info(f"All data saved to {output_file}")
        print(f"All data saved to {output_file}")

    except Exception as e:
        logging.error(f"Error navigating Visits page or scraping: {e}")
        print(f"Error navigating Visits page or scraping: {e}")

def scrape_test_results(driver, output_file):
    """
    Scrape all test results from the test results page and save them to a JSON file.
    Each test result includes its name and scraped content.
    """
    try:
        with open(output_file, "w") as f:
            json.dump([], f, indent=4)
        print(f"{output_file} has been cleared for a fresh scrape.")

        # Navigate to the Test Results page
        test_results_url = "https://mychart.uwhealth.org/MyChart/app/test-results"
        driver.get(test_results_url)
        print("Navigated to Test Results page.")
        logging.info("Navigated to Test Results page.")

        # Wait for the page to load and check for test result clickable links
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'ResultDetailsLink')]"))
        )
        print("Page loaded. Checking for test result links...")

        # Find all clickable test result links
        test_result_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'ResultDetailsLink')]")
        print(f"Found {len(test_result_links)} test result links.")

        if not test_result_links:
            print("No test result links found.")
            logging.info("No test result links found.")
            return

        for i, link in enumerate(test_result_links):
            try:
                test_result_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'ResultDetailsLink')]")
                link = test_result_links[i]

                test_name = link.text.strip()
                print(f"Clicking test result link {i + 1}: {test_name}...")
                logging.info(f"Clicking test result link {i + 1}: {test_name}.")

                link.click()

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "resultNameHeading"))
                )
                print(f"Test details page {i + 1} loaded.")

                soup = BeautifulSoup(driver.page_source, "html.parser")
                data = soup.get_text()

                new_entry = {
                    "test_name": test_name,
                    "content": data
                }

                with open(output_file, "r+") as f:
                    existing_data = json.load(f)
                    existing_data.append(new_entry)
                    f.seek(0)
                    json.dump(existing_data, f, indent=4)

                print(f"Added test result {test_name} to {output_file}.")

                driver.back()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'ResultDetailsLink')]"))
                )
                print("Returned to Test Results page.")

            except Exception as e:
                logging.error(f"Error scraping test result {i + 1}: {e}")
                print(f"Error scraping test result {i + 1}: {e}")

        logging.info(f"All data saved to {output_file}")
        print(f"All data saved to {output_file}")

    except Exception as e:
        logging.error(f"Error navigating Test Results page or scraping: {e}")
        print(f"Error navigating Test Results page or scraping: {e}")


def main():
    """Main function to log in and scrape visits data."""
    driver = setup_driver()
    try:
        login(driver)
        print("Login successful! Page title:", driver.title)
        
        navigate_and_scrape_visits(driver, "data/visits_notes.json")
        scrape_test_results(driver, "data/test_results.json")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
