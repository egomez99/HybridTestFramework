from pytest_bdd import then, parsers
import json


def pytest_bdd_before_scenario(request, feature, scenario):
    if feature.filename.__contains__('login'):
        print('Init Login object')
        test_object = LoginDetails().status_contents


class LoginDetails:
    status_contents = {}

    def __init__(self):
        self.status_contents = '1'