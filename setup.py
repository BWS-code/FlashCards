import io
import argparse

# cards start up db
my_cards = {}

# cards front/back definitions
my_template = [
    'card',
    'definition of the card'
]

# logging method via memory (StringIO) or directly to file (file creation upon start up)
log_methods = [io.StringIO(), 'default.txt']
my_log = log_methods[0]

# parser scope and args
parser = argparse.ArgumentParser()
parser.add_argument('--import_from', default=None)
parser.add_argument('--export_to', default=None)
args = parser.parse_args()