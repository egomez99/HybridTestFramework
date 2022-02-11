import json

import requests
from pytest_bdd import scenarios, given, when, parsers, then

import test_utils
from test_utils import js_globals

scenarios('../../features/backend/chucknorris_jokes_categories.feature')


#FEATURE: Chuck Norris Basic Random Jokes
@given('the chuck norris service contains a payload')
def request_post_service_random_jokes():
    url = 'https://%s/%s' % (test_utils.js_globals.base_url, test_utils.js_globals.get_endpoint_jokes_random)
    test_utils.js_globals.js_globals.rest_response = requests.get(url, headers=test_utils.js_globals.headers)
    print(':: Response: ' + test_utils.js_globals.js_globals.rest_response.text)
    json_response = json.loads(test_utils.js_globals.js_globals.rest_response.text)
    if json_response is not None and 'message' in json_response:
        if json_response['message'].__contains__('Key doesn\'t exists'):
            print("Check your x-rapidapi-key")
        else:
            print('Unexpected message occurred: ' + str(json_response['message']))
    else:
        #item.set_id(str(int(item.attributes['item']['skuId']) + 1))
        print("Received response: "+ str(json_response))


@then(parsers.parse('the response is "{response_type}"'))
def response_success(response_type):
    print(f'Type: {response_type} Status Code: {js_globals.rest_response.status_code}')
    assert js_globals.rest_response.status_code == 200, js_globals.rest_response.text

@given('the chuck norris service contains categories')
def request_post_service_jokes_categories():
    url = 'https://%s/%s' % (test_utils.js_globals.base_url, test_utils.js_globals.get_endpoint_jokes_categories)
    test_utils.js_globals.rest_response = requests.get(url, headers=test_utils.js_globals.headers)
    print(':: Response: ' + test_utils.js_globals.rest_response.text)
    json_response = json.loads(test_utils.js_globals.rest_response.text)
    if 'message' in json_response:
        if json_response['message'].__contains__('Key doesn\'t exists'):
            print("Check your x-rapidapi-key")
        else:
            print('Unexpected message occurred: ' + str(json_response['message']))
    else:
        print("Received response: "+ str(json_response))


@when(parsers.parse('the categories are "{animal}", "{career}"'))
def verify_jokes_categories(animal, career):
    assert 'animal' == animal
    assert 'career' == career
#Received response: ['animal', 'career', 'celebrity', 'dev', 'explicit', 'fashion', 'food', 'history', 'money', 'movie', 'music', 'political', 'religion', 'science', 'sport', 'travel']
