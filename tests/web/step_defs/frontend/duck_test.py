import test_utils

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driverChrome = webdriver.Chrome(ChromeDriverManager().install())




# Scenarios
scenarios('../../features/frontend/duck.feature')


# Fixtures
@pytest.fixture
def browser_instance():
    browser = driverChrome
    browser.implicitly_wait(10)
    yield browser
    browser.quit()


# Given Steps
@given('the DuckDuckGo home page is displayed')
def ddg_home(browser_instance):
    browser_instance.get(test_utils.js_globals.DUCKDUCKGO_HOME)


# When Steps
@when(parsers.parse('the user searches for "{phrase}"'))
def search_phrase(browser_instance, phrase):
    search_input = browser_instance.find_element_by_id('search_form_input_homepage')
    search_input.send_keys(phrase + Keys.RETURN)


# Then Steps
@then(parsers.parse('results are shown for "{phrase}"'))
def search_results(browser_instance, phrase):
    # Check search result list
    # (A more comprehensive test would check results for matching phrases)
    # (Check the list before the search phrase for correct implicit waiting)
    links_div = browser_instance.find_element_by_id('links')
    assert len(links_div.find_elements_by_xpath('//div')) > 0
    # Check search phrase
    search_input = browser_instance.find_element_by_id('search_form_input')
    assert search_input.get_attribute('value') == phrase