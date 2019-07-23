from urllib.parse import parse_qs

import pymysql
import pymysql.cursors

from entry_points import run_from_cli

DESCRIPTION = 'Get result from a PostgreSQL query, with parameters.'

ARG_DEFINITIONS = {
    'MYSQL_DB_USER': 'Username for MySQL connection.',
    'MYSQL_DB_HOST': 'Host for MySQL connection.',
    'MYSQL_DB_PORT': 'Port for MySQL connection.',
    'MYSQL_DB_PASS': 'Pass for MySQL connection.',
    'MYSQL_DB_NAME': 'Database name for MySQL.',
    'QUERY': 'SQL for query.',
    'SQL': 'File containing SQL for query.',
    'PARAMS': 'Query string formatted list of name=value parameters.'
}

REQUIRED_ARGS = [
    'MYSQL_DB_USER', 'MYSQL_DB_HOST', 'MYSQL_DB_PORT', 'MYSQL_DB_PASS',
    'MYSQL_DB_NAME', 'PARAMS'
]

def main(args) -> list:
    if args.SQL:
        with open(args.SQL) as input_file:
            args.QUERY = input_file.read()
    elif not args.QUERY:
        print('QUERY or SQL parameter required, both missing.')
        return []
    params = parse_qs(args.PARAMS)
    for key, value in params.items():
        args.QUERY = args.QUERY.replace('{{%s}}' % key, value[0])
    connection = pymysql.connect(
        host=args.MYSQL_DB_HOST,
        user=args.MYSQL_DB_USER,
        password=args.MYSQL_DB_PASS,
        db=args.MYSQL_DB_NAME,
        port=args.MYSQL_DB_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(args.QUERY)
            return cursor.fetchall()
        finally:
            connection.close()
    return []

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
