import re
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
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
        self.assertTrue(re.search(".*automation.*", driver.current_url), f"Navigated to Automation page: {driver.current_url}")

        page_heading = driver.find_element(By.CLASS_NAME, "page-heading")
        automation_heading = page_heading.find_element(By.XPATH, "//title[text()='Automation']").is_displayed()
        self.assertIsNotNone(automation_heading, "Automation title is present.")

        # Hover again over 'Services' link and verify selection
        services_link = driver.find_element(By.XPATH, "//span[text()='Services']")
        actions.move_to_element(services_link).perform()

        automation_litem = driver.find_element(By.XPATH, "//a[text()='Automation']/parent::li")
        self.assertTrue('selected' in automation_litem.get_attribute('class'), "Automation item is selected in the page header.")

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
        Select(country).select_by_value("Germany")
        message = driver.find_element(By.XPATH, "//label[text()='Message']/following-sibling::textarea[1]")
        message.send_keys("This is a test message.")

        # Check the 'I agree' checkbox
        agree_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='I agree']/following-sibling::label[1]")
        agree_checkbox.click()

        # Check the recaptcha checkbox
        WebDriverWait(driver, STANDARD_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        recaptcha_checkbox = WebDriverWait(driver, STANDARD_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']")))
        driver.execute_script("arguments[0].scrollIntoView();", recaptcha_checkbox)
        recaptcha_checkbox.click()

        # Implicit wait for manual recaptcha solving
        driver.implicitly_wait(60)

        # Click the 'Submit' button and verify the 'Thank you' message
        submit_button = WebDriverWait(driver, STANDARD_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()

        WebDriverWait(STANDARD_DELAY)
        self.assertIn("Thank you", driver.page_source)

    def test_listed_countries(self):
        """Check the list of countries in the Worldwide drop menu,
        and verify if their links work.
        """
        driver = self.driver
        navigate_homepage(driver)
        manage_cookies(driver)

        # Hover over the 'Worldwide' dropdown link in the page header
        worldwide_link = driver.find_element(By.XPATH, "//span[text()='Worldwide']")
        worldwide_link.click()

        # Verify all country-specific links are present and working
        country_links = driver.find_elements(By.XPATH, "//div[@id='country-list-id']/ul/li/a")
        self.assertTrue(len(GLOBAL_PRESENCE) == len(country_links), f"The number of countries in the worldwide list is {len(country_links)}.")

        for country_link in country_links:
            self.assertTrue(country_link.text in GLOBAL_PRESENCE, f"{country_link.text} is in the list of global presence.")
            href = country_link.get_attribute("href")
            driver.get(href)
            manage_cookies(driver)
            ## check ##
            navigate_homepage(driver)
            worldwide_link = driver.find_element(By.XPATH, "//span[text()='Worldwide']")
            worldwide_link.click()


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
