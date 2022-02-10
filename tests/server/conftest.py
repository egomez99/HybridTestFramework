from os.path import join, dirname, realpath
from pytest_bdd import then, parsers

import platform
import json
import time


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(join(dirname(dirname(realpath(__file__))), 'test_utils'))

#import js_globals

#import os, sys
#from os.path import dirname, join, abspath
#sys.path.insert(0, abspath(join(dirname(__file__), '..')))

# import pandas as pd

#from test_utils import js_globals, js_helper, js_properties

@then(parsers.parse('an error occurs containing the message "{error_message}"'))
def verify_error_message(error_message):
    json_result = js_helper.get_message(js_globals.test_object['unique_id'])
    print(json.dumps(json_result))
    assert 'stackTrace' in json_result, 'Expected an error, but none received'
    assert json_result['stackTrace'].__contains__(error_message), 'Did not find expected error ' + error_message + \
                                                                  ' in ' + json_result['stackTrace']

@then(parsers.parse('the response is "{result}"'))
def response_success(result):
    print('FOR: ' + result + ' - Status Code: ' + str(js_globals.rest_response.status_code))
    assert js_globals.rest_response.status_code == 200, js_globals.rest_response.text
    assert js_globals.rest_response.headers["Content-Type"] == "application/json;charset=UTF-8"


@then(parsers.parse('the rest call fails with return code "{ret_code}"'))
def rest_failure(ret_code):
    assert js_globals.rest_response.status_code == int(ret_code)


@then(parsers.parse('the rest message contains "{err_message}"'))
def rest_message_failure(err_message):
    assert err_message in js_globals.rest_response.text


@then(parsers.parse('the {log_type} tlog contains the string'))
def verify_in_tlog(log_type):
    found = verify_tlog(log_type)
    error_message = 'Did not find expected string in %s tlog' % log_type
    assert found, error_message


@then(parsers.parse('the {log_type} tlog does not contain the string'))
def verify_not_in_tlog(log_type):
    found = verify_tlog(log_type)
    error_message = 'Found unexpected string in %s tlog' % log_type
    assert not found, error_message


def verify_tlog(log_type):
    found = False
    if platform.platform().__contains__('Windows'):
        print('Verifying tlog is not supported on Windows')
    else:
        end = time.time() + js_properties.wait_time
        while time.time() < end:
            if log_type == 'suspend':
                print('Searching for ' + js_globals.append_strings[0])
                found = search_tlog(log_type, js_globals.append_strings[0])
                if found:
                    break
            else:
                for message in js_globals.append_strings:
                    print('Searching for string ' + message)
                    for letter in 'abc':
                        found = search_tlog(letter, message)
                        if found:
                            break
                    if found:
                        break
        return found


def search_tlog(postfix, search_string):
    file_helper.copy_tlog_to_f(postfix)
    file_helper.get_file_from_remote('/cdrive/f_drive/tlog.dat', 'tlog.dat')
    found = file_helper.search_file_for_text('tlog.dat', search_string)
    file_helper.delete_file('tlog.dat')
    return found

# @then('the suspend tlog contains the string')
# def verify_suspend_tlog(looking=True):
#     found = False
#     if platform.platform().__contains__('Windows'):
#         print('Verifying tlog is not supported on Windows')
#     else:
#         end = time.time() + js_properties.wait_time
#         while time.time() < end:
#             print('Searching for ' + js_globals.append_strings[0])
#             file_helper.copy_tlog_to_f('suspend')
#             file_helper.get_file_from_remote('/cdrive/f_drive/tlog.dat', 'tlog.dat')
#             found = file_helper.search_file_for_text('tlog.dat', js_globals.append_strings[0])
#             file_helper.delete_file('tlog.dat')
#             if found:
#                 break
#         assert found == looking, 'Did not find expected string in suspend tlog'
#
#
# @then('the suspend tlog does not contain the string')
# def verify_not_in_suspend_tlog():
#     found = False
#     if platform.platform().__contains__('Windows'):
#         print('Verifying tlog is not supported on Windows')
#     else:
#         end = time.time() + js_properties.wait_time
#         while time.time() < end:
#             file_helper.copy_tlog_to_f('suspend')
#             file_helper.get_file_from_remote('/cdrive/f_drive/tlog.dat', 'tlog.dat')
#             print('Searching for ' + js_globals.append_strings[0])
#             found = file_helper.search_file_for_text('tlog.dat', js_globals.append_strings[0])
#             file_helper.delete_file('tlog.dat')
#             if found:
#                 break
#         assert not found, 'Found unexpected string in transaction tlog'
#
#
# @then('the transaction tlog does not contain the string')
# def verify_not_in_transaction_tlog():
#     found = False
#     if platform.platform().__contains__('Windows'):
#         print('Verifying tlog is not supported on Windows')
#     else:
#         end = time.time() + js_properties.wait_time
#         while time.time() < end:
#             for message in js_globals.append_strings:
#                 print('Searching for string ' + message)
#                 for letter in 'abc':
#                     file_helper.copy_tlog_to_f(letter)
#                     file_helper.get_file_from_remote('/cdrive/f_drive/tlog.dat', 'tlog.dat')
#                     found = file_helper.search_file_for_text('tlog.dat', message)
#                     file_helper.delete_file('tlog.dat')
#                     if found:
#                         break
#                 if found:
#                     break
#         assert not found, 'Found unexpected string in suspend tlog'
