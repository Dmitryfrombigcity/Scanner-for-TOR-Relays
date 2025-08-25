import argparse
import sys
from argparse import Namespace

parser = argparse.ArgumentParser()
parser.add_argument(
    '-g',
    '--guard',
    dest='guard_relays',
    action='store_const',
    const=True,
    default=False,
    help='display only relays with positive guard_probability'
)
parser.add_argument(
    '-b',
    '--bandwidth',
    dest='bandwidth',
    action='store_const',
    const=True,
    default=False,
    help='display only relays with positive advertised_bandwidth'
)
parser.add_argument(
    '-t',
    '--top',
    dest='top',
    action='store_const',
    const=True,
    default=False,
    help='display only the top five relays and input templates'
)
parser.add_argument(
    '-s',
    '--silent',
    dest='silent',
    action='store_const',
    const=True,
    default=False,
    help='not display the progress bar'
)
parser.add_argument(
    '-o',
    '--orbot',
    dest='orbot',
    action='store_const',
    const=True,
    default=False,
    help='display only bridges for Orbot'
)
parser.add_argument(
    '-r',
    '--browser',
    dest='browser',
    action='store_const',
    const=True,
    default=False,
    help='display only bridges for Tor'
)

if sys.argv[0][-6:] == "pytest":
    args = Namespace()
else:
    args = parser.parse_args()


