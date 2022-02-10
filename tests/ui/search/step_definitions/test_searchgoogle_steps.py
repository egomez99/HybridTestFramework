import pytest
from pytest_bdd import scenario, scenarios, given, when, then, parsers
import logging, unittest

from selenium import webdriver

logger = logging.getLogger(__name__)
driver = webdriver.Chrome
scenarios('../features/SearchGoogle.feature')


class SearchGoogle(unittest.TestCase):
    def test_method1(self):
        assert True

    # FIXTURES
    @pytest.fixture
    def driver_init(param):
        web_driver = webdriver.Chrome()
        if param == "chrome":
            web_driver = webdriver.Chrome()
        elif param == "firefox":
            web_driver = webdriver.Firefox()
        yield
        web_driver.close()


    def go_to_page(url_page):
        driver.get(url_page)
        driver.implicitly_wait(10)


# STEPS
@given('I am on Google Homepage')
def open_homepage(self):
    logger.info("Google Homepage")
    pass


@when('I add text to search box')
def response_success(self):
    logger.info("Page loaded")
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
