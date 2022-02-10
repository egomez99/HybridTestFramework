from pytest_bdd import then, parsers
import json


def pytest_bdd_before_scenario(request, feature, scenario):
    if feature.filename.__contains__('chuck_norris'):
        print('Init Chuck Norris object: ' + feature.filename)
        print('Request ' + str(request))
        print('Scenario ' + str(scenario))
        test_object = ChuckNorrisDetails().status_contents


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    print('Step Executed call:' + str(step))


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step failed: {step}')


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    print('Before Step Executed:' + str(step))


def pytest_bdd_after_step(request, feature, scenario, step, step_func):
    print('After Step Executed:' + str(step))


class ChuckNorrisDetails:
    status_contents = {}

    def __init__(self):
        self.status_contents = '1'
