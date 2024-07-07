import re
import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import (start_chromedriver, navigate_homepage, manage_cookies,
                    GLOBAL_PRESENCE, STANDARD_TIMEOUT, STANDARD_DELAY)


class TestHomepage(unittest.TestCase):
    """A class for Sogeti's website UI automation test cases."""
    def setUp(self):
        self.driver = start_chromedriver()

    def test_automation_navigation(self):
        """Verify navigation and selection of Automation page
        in the navigation bar.
        """
        driver = self.driver
        navigate_homepage(driver)
        manage_cookies(driver)
        actions = ActionChains(driver)

        # Hover over 'Services' link
        services_link = driver.find_element(By.XPATH, "//span[text()='Services']")
        actions.move_to_element(services_link).perform()

        # Click 'Automation' link
        automation_link = driver.find_element(By.XPATH, "//a[text()='Automation']")
        automation_link.click()

        # Verify navigation to Automation page
        if not re.search(".*automation.*", driver.current_url):
            self.assertFalse(f"Failed to navigate to Automation page: {driver.current_url}")
            return

        self.assertTrue(f"Navigated to Automation page: {driver.current_url}")

        page_heading = driver.find_element(By.CLASS_NAME, "page-heading")
        automation_heading = page_heading.find_element(By.XPATH, "//title[text()='Automation']").is_displayed()
        self.assertIsNotNone(automation_heading, "Automation title is present.")

        # Hover again over 'Services' link and verify selection
        actions.move_to_element(services_link).perform()
        ## check ##
        self.assertTrue(automation_link.is_displayed())

    def test_contact_form(self):
        """Validate the functionality of the 'Contact us' form."""
        driver = self.driver
        navigate_homepage(driver)
        manage_cookies(driver)
        actions = ActionChains(driver)

        # Hover over 'Services' link
        services_link = driver.find_element(By.XPATH, "//span[text()='Services']")
        actions.move_to_element(services_link).perform()

        # Click 'Automation' link
        automation_link = driver.find_element(By.XPATH, "//a[text()='Automation']")
        automation_link.click()

        # Scroll down to 'Contact us' form
        contact_form = driver.find_element(By.CLASS_NAME, "Form__MainBody")
        driver.execute_script("arguments[0].scrollIntoView();", contact_form)

        # Fill the form with random data
        first_name = driver.find_element(By.XPATH, "//label[text()='First Name']/following-sibling::input[1]")
        first_name.send_keys("John")
        last_name = driver.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::input[1]")
        last_name.send_keys("Doe")
        email = driver.find_element(By.XPATH, "//label[text()='Email']/following-sibling::input[1]")
        email.send_keys("john.doe@example.com")
        phone = driver.find_element(By.XPATH, "//label[text()='Phone']/following-sibling::input[1]")
        phone.send_keys("1234567890")
        company = driver.find_element(By.XPATH, "//label[text()='Company']/following-sibling::input[1]")
        company.send_keys("Sogeti")
        country = driver.find_element(By.XPATH, "//label[text()='Country']/following-sibling::div[1]//select")
        country.select_by_visible_text("Germany")
        message = driver.find_element(By.XPATH, "//label[text()='Message']/following-sibling::textarea[1]")
        message.send_keys("This is a test message.")

        # Check the 'I agree' checkbox
        agree_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='I agree']")
        agree_checkbox.click()

        # Click recaptcha and hope it works :)
        WebDriverWait(driver, STANDARD_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, STANDARD_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

        # Click the 'Submit' button and verify the 'Thank you' message
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        time.sleep(STANDARD_DELAY)
        self.assertIn("Thank you", driver.page_source)

    def test_listed_countries(self):
        """Check the list of countries in the Worldwide drop menu,
        and verify if their links work.
        """
        driver = self.driver
        navigate_homepage(driver)
        manage_cookies(driver)
        actions = ActionChains(driver)

        # Hover over the 'Worldwide' dropdown link in the page header
        worldwide_link = driver.find_element(By.XPATH, "//*[text()='Worldwide']")
        actions.move_to_element(worldwide_link).perform()

        # Verify all country-specific links are present and working
        country_links = driver.find_elements(By.XPATH, "//div[@id='country-list-id']/ul/li/a")

        if len(GLOBAL_PRESENCE) == len(country_links):
            self.assertTrue(f"The number of countries in the worldwide list is {len(GLOBAL_PRESENCE)}.")
        else:
            self.assertFalse(f"The expected list of countries has {len(GLOBAL_PRESENCE)} countries,"
                             f"while the current list has {len(country_links)} countries.")

        for country_link in country_links:
            if country_link.text in GLOBAL_PRESENCE:
                href = country_link.get_attribute("href")
                driver.get(href)
                manage_cookies(driver)
                ## check ##
                navigate_homepage(driver)
            else:
                self.assertFalse(f"{country_link.text} is not a country in the list of global presence.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
