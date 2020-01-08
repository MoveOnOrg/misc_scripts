from datetime import datetime, timedelta
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
    'DB_NAME': 'Database name'
}

REQUIRED_ARGS = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME'
]

def table_date(table):
    ts = int(''.join([char for char in list(table) if char.isdigit()]))
    return datetime.utcfromtimestamp(ts)

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print(('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg)))
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
        tables_query = """
        SET search_path TO 'signature_propensity';
        SELECT DISTINCT(tablename)
        FROM pg_table_def
        WHERE (
            tablename LIKE 'global_sig_prop_targets%'
            OR tablename LIKE 'prop_targets%'
        )
        AND tablename NOT LIKE '%_pkey'
        """
        database_cursor.execute(tables_query)
        tables_result = list(database_cursor.fetchall())
        tables = [table.get('tablename') for table in tables_result]
        table_dates = {}
        for table in tables:
            table_dates[table] = table_date(table)
        today = datetime.today()
        month_ago = today - timedelta(days=30)
        old_tables = [table for table in list(table_dates.keys()) if table_dates[table] < month_ago][:100]
        for table in old_tables:
            database_cursor.execute("""
            DROP TABLE signature_propensity.%s
            """ % table)
        database.commit()
        database_cursor.close()
        return old_tables

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description='Drop old signature propensity tables.'
    )
    pp = pprint.PrettyPrinter(indent=2)

    for argname, helptext in list(ARG_DEFINITIONS.items()):
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pp.pprint(main(args))
