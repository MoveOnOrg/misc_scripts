import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'CSV': 'CSV of donation records.'
}

REQUIRED_ARGS = [
    'CSV'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        donations = []
        with open(args.CSV, 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                date = row.get('donation_date')
                donations.append(float(row.get('donation_amount', 0)))
        return 'New import for %s: *%s* donations totalling *$%s*.' % (date, len(donations), "{0:.2f}".format(sum(donations)))

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Get summary of donations.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
