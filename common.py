"""Common library file used for constants, enums and functions."""
import os
import platform
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Site Constants
HOMEPAGE = "https://www.sogeti.com/"
GLOBAL_PRESENCE = ["BELGIUM", "FINLAND", "FRANCE", "GERMANY", "IRELAND", "LUXEMBOURG",
                   "NETHERLANDS", "NORWAY", "SPAIN", "SWEDEN", "UK", "USA"]

# Project Constants
STANDARD_TIMEOUT = 10
STANDARD_DELAY = 5


# Common Functions
def start_chromedriver():
    """Initial call for a testscript function."""
    # Determine the operating system
    os_type = platform.system()

    # Set the relative path for the ChromeDriver based on the operating system
    if os_type == 'Windows':
        relative_chromedriver_path = 'drivers/chromedriver-win64.exe'
    elif os_type == 'Darwin':  # 'Darwin' is the system name for macOS
        relative_chromedriver_path = 'drivers/chromedriver-mac'
    else:
        raise Exception(f"Unsupported operating system: {os_type}")

    # Convert the relative path to an absolute path
    project_path = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(project_path, relative_chromedriver_path)

    # Set ChromeDriver path and disable automation flags
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def navigate_homepage(driver):
    """Navigate to the homepage defined as a class constant."""
    driver.get(HOMEPAGE)


def manage_cookies(driver):
    """Set the cookie policy to: Accept all cookies."""
    try:
        div_cookie_consent = WebDriverWait(driver, STANDARD_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "CookieConsent")))
        div_cookie_consent.find_element(By.XPATH, "//button[@class='acceptCookie']").click()

    except TimeoutException:
        print("Cookie consent div is not visible.")
