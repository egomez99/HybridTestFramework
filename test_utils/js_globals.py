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

# Constants
DUCKDUCKGO_HOME = 'https://duckduckgo.com/'
GOOGLE_HOME = 'https://www.google.com/'

# Features:
# chucknorris_jokes_categories.feature
# chucknorris_basic_random_joke.feature
headers = {"content-type": "application/json;charset=UTF-8",
           "x-rapidapi-key": "yzHJio19EpmshLytTZbDBcJnVHiOp1kH3NYjsnbSXBINUshTqv"}
base_url = 'matchilling-chuck-norris-jokes-v1.p.rapidapi.com'
get_endpoint_jokes_random = '/jokes/random'
get_endpoint_jokes_categories = '/jokes/categories'

