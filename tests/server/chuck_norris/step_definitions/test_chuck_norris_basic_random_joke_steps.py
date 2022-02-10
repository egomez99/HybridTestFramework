import json

import requests
from pytest_bdd import scenarios, given, when, then, parsers

from test_utils import js_globals
import logging

logger = logging.getLogger(__name__)

headers = {"content-type": "application/json;charset=UTF-8",
           "x-rapidapi-key": "yzHJio19EpmshLytTZbDBcJnVHiOp1kH3NYjsnbSXBINUshTqv"}
base_url = 'matchilling-chuck-norris-jokes-v1.p.rapidapi.com'
get_endpoint_jokes_random = '/jokes/random'
get_endpoint_jokes_categories = '/jokes/categories'

scenarios('../features')


# FEATURE: Chuck Norris Basic Random Jokes
@given('the chuck norris service contains a payload')
def request_post_service_random_jokes():
    url = 'https://%s/%s' % (base_url, get_endpoint_jokes_random)
    js_globals.rest_response = requests.get(url, headers=headers)
    print(':: Response: ' + js_globals.rest_response.text)
    json_response = json.loads(js_globals.rest_response.text)
    if json_response is not None and 'message' in json_response:
        if json_response['message'].__contains__('Key doesn\'t exists'):
            print("Check your x-rapidapi-key")
        else:
            print('Unexpected message occurred: ' + str(json_response['message']))
    else:
        # item.set_id(str(int(item.attributes['item']['skuId']) + 1))
        print("Received response: " + str(json_response))


@then(parsers.parse('the response is "{result}"'))
def response_success(result):
    info = 'FOR: ' + result + ' - Status Code: ' + str(js_globals.rest_response.status_code)
    logger.info(info)
    assert js_globals.rest_response.status_code == 200, js_globals.rest_response.text
    assert js_globals.rest_response.headers["Content-Type"] == "application/json;charset=UTF-8"


@given('the chuck norris service contains categories')
def request_post_service_jokes_categories():
    url = 'https://%s/%s' % (base_url, get_endpoint_jokes_categories)
    js_globals.rest_response = requests.get(url, headers=headers)
    print(':: Response: ' + js_globals.rest_response.text)
    json_response = json.loads(js_globals.rest_response.text)
    if 'message' in json_response:
        if json_response['message'].__contains__('Key doesn\'t exists'):
            print("Check your x-rapidapi-key")
        else:
            print('Unexpected message occurred: ' + str(json_response['message']))
    else:
        print("Received response: " + str(json_response))


@when(parsers.parse('the categories are "{animal}", "{career}"'))
def verify_jokes_categories(animal, career):
    assert 'animal' == animal
    assert 'career' == career
# Received response: ['animal', 'career', 'celebrity', 'dev', 'explicit', 'fashion', 'food', 'history', 'money', 'movie', 'music', 'political', 'religion', 'science', 'sport', 'travel']
