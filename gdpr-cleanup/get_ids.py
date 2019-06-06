import csv

import psycopg2
import psycopg2.extras

from entry_points import run_from_cli


DESCRIPTION = 'Get some IDs from database.'

ARG_DEFINITIONS = {
    'COUNT': 'Number of IDs to get.',
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'DB_TABLE': 'Database table (with schema prefix)',
    'OUT': 'Output CSV file with user_id column.'
}

REQUIRED_ARGS = [
    'COUNT', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'DB_TABLE',
    'OUT'
]

def main(args) -> str:
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
    query = """
    SELECT ak_id AS user_id
    FROM %s
    WHERE ak_id IS NOT NULL
    ORDER BY random()
    LIMIT %s""" % (args.DB_TABLE, args.COUNT)
    database_cursor.execute(query)
    results = list(database_cursor.fetchall())

    with open(args.OUT, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=['user_id'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    return args.OUT


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
