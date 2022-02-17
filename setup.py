import argparse


# cards start up db
my_cards = {}

# cards front/back definitions
my_template = [
    'card',
    'definition of the card'
]

# parser scope and args
parser = argparse.ArgumentParser()
parser.add_argument('--import_from', default=None)
parser.add_argument('--export_to', default=None)
args = parser.parse_args()
