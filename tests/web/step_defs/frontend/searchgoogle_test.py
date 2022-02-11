import logging

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import test_utils
from test_utils import js_globals

driverChrome = webdriver.Chrome(ChromeDriverManager().install())


logger = logging.getLogger(__name__)

# Fixtures
@pytest.fixture
def browser_instance():
    browser = driverChrome
    browser.implicitly_wait(10)
    yield browser
    browser.quit()


scenarios('../../features/frontend/searchgoogle.feature')

# class SearchGoogle(unittest.TestCase):
#     def test_method1(self):
#         assert True
#
#     # FIXTURES
#     @pytest.fixture
#     def driver_init(param):
#         web_driver = webdriver.Chrome()
#         if param == "chrome":
#             web_driver = webdriver.Chrome()
#         elif param == "firefox":
#             web_driver = webdriver.Firefox()
#         yield
#         web_driver.close()


# STEPS
@given('I am on Google Homepage')
def open_homepage(browser_instance):
    logger.info("Google Homepage")
    browser_instance.get(test_utils.js_globals.GOOGLE_HOME)
    pass


@when(parsers.parse('I search for "{searching_term}"'))
def search_for(browser_instance, searching_term):
    logger.info(f"Searching: {searching_term}")
    search_input = browser_instance.find_element_by_name('q')
    search_input.send_keys(searching_term + Keys.RETURN)
    pass


@then(parsers.parse('I check results for "{searching_term}"'))
def check_results_for(browser_instance, searching_term):
    logger.info(f"Searching: {searching_term}")

    results_stats = browser_instance.find_element(By.ID, 'result-stats')
    assert len(results_stats.find_elements_by_xpath('//div')) > 0

    links_div = browser_instance.find_element_by_id('rso')
    assert len(links_div.find_elements_by_xpath('//div')) > 0
    pass


# @pytest.mark.usefixtures("driver_init")
# class BasicTest:
#    pass


# class Test_URL1(BasicTest1):
#     def test_open_url(self):
#         self.driver.get(ODE12)
#         print(self.driver.title)
#         sleep(1)
#         elem = self.driver.find_element_by_name("username")
#         elem.clear()
#         elem.send_keys(USERNAME)
#         elem.send_keys(Keys.RETURN)
#         sleep(4)
#         elem = self.driver.find_element_by_name("password")
#         elem.clear()
#         elem.send_keys(PASSWORD)
#         elem.send_keys(Keys.RETURN)
#         assert "Results found" not in self.driver.page_source
#         sleep(7)


# class Test_URL(BasicTest):
#     def test_open_url(self):
#         self.driver.get(test_utils.js_properties.ODE12)
#         self.driver.implicitly_wait(10)  # seconds
#         try:
#             elem = self.driver.find_element_by_id("username")
#             elem.clear()
#             elem.send_keys(test_utils.js_properties.USERNAME)
#             elem.send_keys(Keys.RETURN)
#
#             elem = self.driver.find_element_by_id("password")
#             elem.clear()
#             elem.send_keys(test_utils.js_properties.PASSWORD)
#             elem.send_keys(Keys.RETURN)
#
#         finally:
#             pass
#
#         assert "Results found" not in self.driver.page_source
#         sleep(5)
