from datetime import time
import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="module")
def driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    # Maximize the browser window to full screen
    driver.maximize_window()
    yield driver
    # Teardown - close the WebDriver
    driver.quit()


@pytest.fixture(scope="module")
def homepage_url():
    return "https://useinsider.com/"


@pytest.fixture(scope="module")
def careers_page_url():
    return "https://useinsider.com/careers"


import pytest
from selenium import webdriver
import os


@pytest.fixture(scope="function")
def driver(request):
    # Initialize WebDriver
    driver = webdriver.Chrome()

    # Make sure the WebDriver instance is terminated when tests finish
    def fin():
        driver.quit()

    request.addfinalizer(fin)

    return driver


# Pytest hook to capture screenshots upon test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Fetch the WebDriver instance from the test function
            driver = item.funcargs['driver']

            # Define the path to save the screenshot
            screenshot_path = os.path.join(os.getcwd(), "screenshots", item.name + ".png")

            # Capture the screenshot
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved as {screenshot_path}")
        except Exception as e:
            print(f"\nFailed to capture screenshot: {e}")


def test_verify_homepage_accessibility(driver, homepage_url):
    driver.get(homepage_url)
    assert "Insider" in driver.title  # Check if the homepage title contains "Insider"


def test_navigate_to_careers_page(driver, homepage_url, careers_page_url):
    driver.get(homepage_url)
    # Navigate to Careers page
    company_menu = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Company')]"))
    )
    company_menu.click()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".new-menu-dropdown-layout-6"))
    )
    # Click on the "Company" element to reveal the Careers option
    careers_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[.='Careers']"))
    )
    careers_option.click()
    # Wait until the Careers page is fully loaded
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='button-group d-flex flex-row']/a[.='Find your dream job']")))
    # Verify if the Career page is accessible
    assert "Careers" in driver.title  # Check if the page title contains "Careers"


def test_check_career_page_sections(driver, careers_page_url):
    driver.get(careers_page_url)
    # Verify if the Career page sections are accessible
    career_page_sections = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".page-template"))
    )
    assert career_page_sections, "Career page sections are not accessible."

    # Check if Locations section is accessible
    locations_section = driver.find_elements(By.XPATH, "//div[@class='col-md-6 mt-3 mt-md-0 d-flex justify-content-between justify-content-md-end align-items-end']/a[2]")
    assert locations_section, "Locations section is not accessible."

    # Check if Teams section is accessible
    teams_section = driver.find_elements(By.CSS_SELECTOR, ".btn-outline-secondary")
    assert teams_section, "Teams section is not accessible."

    # Check if Life at Insider section is accessible
    life_at_insider_section = driver.find_elements(By.CSS_SELECTOR, " .swiper-wrapper")
    assert life_at_insider_section, "Life at Insider section is not accessible."

def test_visit_dream_job_page(driver, careers_page_url):
    driver.get(careers_page_url)
    # Accept cookies if present
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )
        cookie_accept_button.click()
    except:
        pass

    # Navigate to the dream job page
    dream_job_link = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group d-flex flex-row']/a[.='Find your dream job']"))
    )
    dream_job_link.click()

# Scroll down the page
    driver.execute_script("document.getElementById('career-position-list').scrollIntoView();")

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

@pytest.mark.parametrize("location, job", [("Istanbul, Turkey", "Quality Assurance")])
def test_select_location_and_job(driver, location, job):
    url = "https://useinsider.com/careers/open-positions/?department=qualityassurance"
    driver.get(url)  # Navigate to the specified URL

    try:
        # Accept cookies if present
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )
        cookie_accept_button.click()
    except:
        pass

        # Scroll down the page
        driver.execute_script("document.getElementById('career-position-list').scrollIntoView();")

    try:
        # Wait for the first element to be clickable
        first_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@id='top-filter-form']/div[1]//span[@class='select2-selection__rendered']"))
        )

        # Click on the first element
        first_element.click()

        # Scroll down to the desired option
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN * 3).perform()  # Adjust the number of arrow down presses as needed

        # Select location
        location_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[.='{location}']"))
        )
        location_option.click()

    except:
       pass


import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("location, job", [("Istanbul, Turkey", "Quality Assurance")])
def test_check_text_on_careers_page(driver, location, job):
    url = "https://useinsider.com/careers/open-positions/?department=qualityassurance"
    driver.get(url)  # Navigate to the specified URL
    try:
        # Find the element containing the article text
        article_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='jobs-list']"))
        )

        # Get the text of the article element
        article_text = article_element.text

        # Define the phrases to check for
        phrases_to_check = ["Istanbul", "qualityassurance"]

        # Check if any of the phrases are present in the article text
        for phrase in phrases_to_check:
            assert phrase not in article_text, f"The article contains the phrase: '{phrase}'"

        print("The article does not contain the phrases 'Istanbul' and 'quality assurance'.")

    except AssertionError as e:
        pytest.fail(f"Assertion error: {e}")

    except Exception as e:
        pytest.fail(f"An error occurred: {e}")


import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.mark.parametrize("location, job", [("Istanbul, Turkey", "Quality Assurance")])
def test_check_job_page_redirect(driver, location, job):
    url = "https://useinsider.com/careers/open-positions/?department=qualityassurance"
    driver.get(url)  # Navigate to the specified URL


    try:
        # Accept cookies if present
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )
        cookie_accept_button.click()
    except:
        pass



    try:
        # Find and click the "View Role" button
        view_role_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://jobs.lever.co/useinsider/6b1cb4da-e2b8-4eff-83b7-2931c44b4e69']"))
        )
        view_role_button.click()

        # Switch to the new window
        WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])

        # Verify the URL of the new page
        assert "https://jobs.lever.co/useinsider/6b1cb4da-e2b8-4eff-83b7-2931c44b4e69" in driver.current_url, \
            "Assertion failed: Clicking the 'View Role' button does not redirect to the Lever Application form page."

        print("Assertion passed: Clicking the 'View Role' button redirects to the Lever Application form page.")

    except TimeoutException:
        pytest.fail("Timeout occurred while waiting for the 'View Role' button to be clickable.")

    except AssertionError as e:
        pytest.fail(f"Assertion error: {e}")

    except Exception as e:
        pytest.fail(f"An error occurred: {e}")

