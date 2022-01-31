from pytest_bdd import scenario, scenarios, given, when, then, parsers
import requests
import json

#Import the modules required for the execution
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

scenarios('../features')

BASE_URL = 'https://ode12.cms.ibm.net/'

PAGE_BUILDER    = 'https://ode12.cms.ibm.net/admin/myworkbench/create-page-items'
ADD_LEADSPACE   = 'https://ode12.cms.ibm.net/node/add/leadspace'

ODE12    = 'https://ode12.cms.ibm.net/admin/myworkbench'
USERNAME = 'eduardo.gomez@ibm.com'
PASSWORD = '...'

@given('I am on "{TARGET_URL}"')
def open_homepage():

    pass


@when('I wait for the page to load')
def response_success():
    print("Page loaded")
    pass


# Fixture for Firefox
@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        web_driver = webdriver.Chrome()
    if request.param == "firefox":
        web_driver = webdriver.Firefox()
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.mark.usefixtures("driver_init")
class BasicTest:
    pass


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


class Test_URL(BasicTest):
    def test_open_url(self):
        self.driver.get(ODE12)
        self.driver.implicitly_wait(10)  # seconds
        try:
            elem = self.driver.find_element_by_id("username")
            elem.clear()
            elem.send_keys(USERNAME)
            elem.send_keys(Keys.RETURN)

            elem = self.driver.find_element_by_id("password")
            elem.clear()
            elem.send_keys(PASSWORD)
            elem.send_keys(Keys.RETURN)

        finally:
            pass

        assert "Results found" not in self.driver.page_source
        sleep(5)