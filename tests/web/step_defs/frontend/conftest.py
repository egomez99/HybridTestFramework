#conftest.py executed from closer to root project folder level by each scenario

import logging
#from webdriver_manager.firefox import GeckoDriverManager
#driverFirefox = webdriver.Firefox(executable_path=GeckoDriverManager().install())

logger = logging.getLogger(__name__)

def pytest_bdd_before_scenario(request, feature, scenario):
    if feature.filename.__contains__('feature'):
        logger.info(f'Init Scenario: {request}')
        test_object = TestDetails().status_contents
        logger.info(f'Test Object: {test_object}')
    else:
        logger.info(f'Error Scenario: {request}')


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    print(f'Step Executed call: {step}')


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step failed: {step}')


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    print(f'Before Step Executed: {step}')


def pytest_bdd_after_step(request, feature, scenario, step, step_func):
    print(f'After Step Executed: {step}')


class TestDetails:
    status_contents = {}

    def __init__(self):
        self.status_contents = '1'