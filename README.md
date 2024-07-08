# Sogeti
This repository contains automated UI tests for Sogeti's website using Selenium and Python.

# Prerequisites
1. [Python 3.x](https://www.python.org/downloads/)
2. [Selenium](https://pypi.org/project/selenium/)
3. Google Chrome
4. ChromeDriver (included in the repo, could be overwritten to be compatible with the installed version of Chrome)

# Setup
1. Clone the repository: 

`git clone <repository-url>`
2. Install the Python package `requests`: 

`pip install requests`

# Running the Tests

To run the tests, execute the following command in the project directory:

`python TestHomepage.py`

This will run all the test cases defined in the TestHomepage.py file.

# Test Cases
## Test Case 1: Automation Navigation
1. Navigate to the Sogeti homepage.
2. Hover over the 'Services' link and click the 'Automation' link.
3. Verify navigating to 'Automation' page and the 'Automation' text is visible.
4. Hover again over the 'Services' link and verify that 'Services' and 'Automation' are selected.

## Test Case 2: Contact Form
1. Navigate to the Sogeti homepage.
2. Hover over the 'Services' link and click the 'Automation' link.
3. Scroll down to the 'Contact us' form.
4. Fill the form with random generated data.
5. Check the 'I agree' checkbox.
6. Delay the next step to allow for human-solving of recaptcha challenge.
7. Click the 'Sumbit' button and verify the 'Thank you' message is displayed.

## Test Case 3: Listed Countries
1. Navigate to the Sogeti homepage.
2. Click the 'Worldwide' dropdown link in the page header.
3. Assert the expected countries and all country-specific Sogeti links are working.
