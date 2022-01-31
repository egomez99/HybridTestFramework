from pytest_bdd import then, parsers
import json


def pytest_bdd_before_scenario(request, feature, scenario):
    if feature.filename.__contains__('chuck_norris'):
        print('Init Chuck Norris object')
        test_object = ChuckNorrisDetails().status_contents


class ChuckNorrisDetails:
    status_contents = {}

    def __init__(self):
        self.status_contents = '1'