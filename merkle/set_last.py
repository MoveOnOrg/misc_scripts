import os
import sys

import psycopg2
import psycopg2.extras

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'LAST_RUN_SCRIPT': 'Script name.',
    'LAST_RUN_DATE': 'Date of last run.'
}

REQUIRED_ARGS = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'LAST_RUN_SCRIPT', 'LAST_RUN_DATE'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        database = psycopg2.connect(
            host=args.DB_HOST,
            port=args.DB_PORT,
            user=args.DB_USER,
            password=args.DB_PASS,
            database=args.DB_NAME
        )
        database_cursor = database.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        last_run_query = """
        UPDATE tech.script_last_run SET last_run = '%s'
        WHERE script = '%s'
        """ % (args.LAST_RUN_DATE, args.LAST_RUN_SCRIPT)
        database_cursor.execute(last_run_query)
        database.commit()
        return args.LAST_RUN_DATE

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Set date of last run.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
