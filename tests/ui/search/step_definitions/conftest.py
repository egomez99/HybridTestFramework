import pytest
import logging

logger = logging.getLogger(__name__)

def pytest_bdd_before_scenario(request, feature, scenario):
    if feature.filename.__contains__('search'):
        logger.info('Init Login object')
        test_object = SearchDetails().status_contents

class SearchDetails:
    status_contents = {}

    def __init__(self):
        self.status_contents = '1'