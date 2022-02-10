import sys
sys.path.append("../")
from os.path import join, dirname, realpath

# global variables
home_dir = dirname(dirname(realpath(__file__)))
expected_values = {}
result = {}
failure_message = ''
to_reset = ''
client = type('', (), {})()
rest_response = {}
test_function = ''
test_object = {}
mcts_order_object = {}
template_object = {}
append_strings = []
active_order = False
test_totals_event = False
active_messages = {}
pos_event_messages = []
keys_dir = join(join(dirname(dirname(realpath(__file__))), 'resources'), 'keys')
scenario_name = ''
