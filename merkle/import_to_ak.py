import os
import sys

from actionkit.api.user import AKUserAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'CSV': 'CSV file to import.',
    'AK_BASEURL': 'ActionKit Base URL.',
    'AK_USER': 'ActionKit API username.',
    'AK_PASSWORD': 'ActionKit API password.',
    'AK_IMPORT_PAGE': 'ActionKit import page name.'
}

REQUIRED_ARGS = [
    'CSV', 'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        api = AKUserAPI(args)
        result = api.bulk_upload(args.AK_IMPORT_PAGE, open(args.CSV, 'rb'), 1)
        return result

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Import file.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
