"""Common library file used for constants, enums and functions."""
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Site Constants
HOMEPAGE = "https://www.sogeti.com/"
GLOBAL_PRESENCE = ["Belgium", "Finland", "France", "Germany", "Ireland", "Luxembourg",
                   "Netherlands", "Norway", "Spain", "Sweden", "UK", "US"]

# Project Constants
CHROMEDRIVER_PATH = "../drivers/chromedriver"

# Time Constants
STANDARD_TIMEOUT = 10
STANDARD_DELAY = 5


# Common Functions
def start_chromedriver():
    """Initial call for a testscript function."""
    # Setting options to enable recaptcha click
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome()
    driver.maximize_window()
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
