import json
import time
import string
from random import choice
from test_utils import js_globals, js_properties

expected_values = {}
message_sent = False


def verify_element(element, actual, expected):
    if actual != expected:
        js_globals.failure_message += 'Found ' + element + ' to be ' + actual + ' but expected ' + expected + ','


def on_message(client, userdata, message):
    print('Message topic %s' % message.topic)
    test_function = message.topic.split('/')[3]

    if test_function == 'alert':
        print('Received an alert from traffic-generator: %s' % json.loads(message.payload.decode('utf-8')))
    elif test_function == 'pos_events' and test_function == js_globals.test_function:
        result = json.loads(message.payload.decode('utf-8'))
        print('Result is %s' % result)
        found = False
        for test_message in js_globals.pos_event_messages:
            print('checking against message id: %s' % test_message['unique_id'])
            if result['unique_id'] == test_message['unique_id']:
                found = True
                break
        if not found and (js_globals.test_totals_event or result['tag'] != 'transactionTotaled'):
            if js_globals.test_totals_event:
                js_globals.test_totals_event = False
            print('Adding result to pos_event_messages list')
            js_globals.pos_event_messages.append(result)
    elif test_function == js_globals.test_function:
        result = json.loads(message.payload.decode('utf-8'))
        print('Result is %s' % result)
        if 'unique_id' in result and result['unique_id'] not in js_globals.active_messages:
            print('Setting global result')
            # js_globals.active_messages.append(result['unique_id'])
            js_globals.active_messages[result['unique_id']] = result
            print('active messages is ')
            print(js_globals.active_messages)


def get_message(unique_id):
    end = time.time() + js_properties.wait_time
    while time.time() < end:
        if unique_id in js_globals.active_messages:
            # js_globals.active_messages.remove(result)
            my_result = js_globals.active_messages[unique_id]
            del js_globals.active_messages[unique_id]
            return my_result
            # for result in js_globals.active_messages:
            # print('get message unique id is ' + result['unique_id'])
            # if result['unique_id'] == unique_id:
            # js_globals.active_messages.remove(result)
            # return result
    js_globals.failure_message = 'No MQTT message received'
    return {'content': 'No MQTT message received'}


def get_pos_event_message(message_type):
    end = time.time() + js_properties.wait_time
    while time.time() < end:
        if len(js_globals.pos_event_messages) > 0:
            for test_message in js_globals.pos_event_messages:
                if test_message['tag'] == message_type:
                    index = js_globals.pos_event_messages.index(test_message)
                    found_message = js_globals.pos_event_messages.pop(index)
                    print('Popped result: %s' % found_message)
                    js_globals.result = found_message
                    return found_message
    js_globals.failure_message = 'No MQTT message received'
    return None


def reset_vars():
    elements = js_globals.to_reset.split(',')
    for x in elements:
        js_globals.expected_values[x] = ''
    js_globals.failure_message = ''
    js_globals.to_reset = ''
    time.sleep(1)


def generate_hash():
    return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
