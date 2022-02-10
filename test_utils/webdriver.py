from selenium import webdriver


class WebDriver:
    def __init__(self):
        self.driver = None

    # Fixture for Firefox
    # @pytest.fixture(params=["chrome", "firefox"], scope="class")
    def driver_init(request):
        if request.param == "chrome":
            web_driver = webdriver.Chrome()
        elif request.param == "firefox":
            web_driver = webdriver.Firefox()
        request.cls.driver = web_driver
        yield
        web_driver.close()

    def go_to_page(self, url_page):
        self.driver.get(url_page)
        self.driver.implicitly_wait(10)  # seconds
