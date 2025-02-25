import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def init(headless: bool = False):
    """
    Initializes the SeleniumBase driver with Undetected Chrome.
    """
    # Pass headless parameter if needed
    return Driver(uc=True, headless=headless)

def login_and_wait(driver):
    """
    Opens the Dune login page and waits for the user to log in.
    """
    url = 'https://dune.com/auth/login'
    logging.info("Navigating to login page...")
    driver.uc_open_with_reconnect(url, reconnect_time=6)
    input("Please login and press Enter to continue...")

def find_first_matching_element(driver):
    """
    Returns the first element among those with class starting with 'visual_statuses__'
    that has text starting with a digit and not ending with 'min', while excluding common words.
    """
    try:
        elements = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'visual_statuses__')]")
        for element in elements:
            text_value = element.text.strip()
            # Check if text starts with a digit and does not contain undesired text
            if re.match(r"^\d+.*[^min]$", text_value) and text_value.lower() not in {"now", "queued"}:
                logging.info(f"Matching element found with text: {text_value}")
                return element
    except Exception as e:
        logging.error("Error while searching for matching element: %s", e)
    logging.warning("No matching element found.")
    return None

def click_element(driver, element):
    """
    Attempts to click on the given element. If normal click fails, uses JavaScript click.
    """
    try:
        element.click()
    except Exception as e:
        logging.warning("Normal click failed (%s). Using JavaScript click...", e)
        driver.execute_script("arguments[0].click();", element)

def click_refresh_results(driver):
    """
    Attempts to find and click the "Refresh results" button.
    Returns True if clicked, otherwise False.
    """
    try:
        refresh_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[starts-with(@class, 'MenuPanel_content__') and text()='Refresh results']")
            )
        )
        logging.info("Found 'Refresh results' button. Clicking...")
        click_element(driver, refresh_button)
        return True
    except Exception as e:
        logging.warning("'Refresh results' button not found or not clickable: %s", e)
        return False

def close_cookie_notification(driver):
    """
    Checks for a cookie notification popup and clicks the 'Accept' button if it is present.
    """
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "CookieNotification_notification__0Nkrk"))
        )
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        logging.info("Cookie notification detected. Clicking 'Accept' button...")
        click_element(driver, accept_button)
        # Wait for the popup to disappear
        time.sleep(2)
    except Exception:
        logging.info("No cookie notification found.")

def refresh_dashboard(driver, url: str):
    """
    Main loop that continually looks for matching elements and triggers a refresh.
    In case of error, the dashboard is reloaded.
    """
    while True:
        try:
            close_cookie_notification(driver)
            # Inner loop to continuously process available elements
            while True:
                time.sleep(1)
                matching_element = find_first_matching_element(driver)
                if matching_element:
                    try:
                        # Attempt to find a button within the matching element
                        button = matching_element.find_element(
                            By.XPATH, ".//*[starts-with(@class, 'IconButton_iconButton__')]"
                        )
                        if button:
                            logging.info("Clicking button inside matching element with text: %s", matching_element.text)
                            click_element(driver, button)
                            if click_refresh_results(driver):
                                logging.info("Refresh triggered. Waiting before next cycle...")
                                time.sleep(10)  # Delay after refresh
                    except Exception as inner_e:
                        logging.warning("No button found within the matching element: %s", inner_e)
                else:
                    # Wait longer if no matching element was found
                    time.sleep(30)
        except Exception as outer_e:
            logging.error("An error occurred: %s. Reloading the dashboard...", outer_e)
            driver.uc_open_with_reconnect(url, reconnect_time=6)

if __name__ == '__main__':
    # Initialize driver
    driver = init(headless=False)
    try:
        # Login phase
        login_and_wait(driver)
        # Navigate to the dashboard
        dashboard_url = 'https://dune.com/flexperps/flexperpetuals-analytics'
        logging.info("Navigating to dashboard: %s", dashboard_url)
        driver.uc_open_with_reconnect(dashboard_url, reconnect_time=6)
        # Start the refresh loop
        refresh_dashboard(driver, dashboard_url)
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user. Exiting...")
    finally:
        driver.quit()
