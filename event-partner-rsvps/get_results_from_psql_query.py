import psycopg2

from entry_points import run_from_cli

DESCRIPTION = 'Get result from a PostgreSQL query.'

ARG_DEFINITIONS = {
    'PSQL_DB_USER': 'Username for PostgreSQL connection.',
    'PSQL_DB_HOST': 'Host for PostgreSQL connection.',
    'PSQL_DB_PORT': 'Port for PostgreSQL connection.',
    'PSQL_DB_PASS': 'Pass for PostgreSQL connection.',
    'PSQL_DB_NAME': 'Database name for PostgreSQL.',
    'QUERY': 'SQL for query.',
    'SQL': 'File containing SQL for query.'
}

REQUIRED_ARGS = [
    'PSQL_DB_USER', 'PSQL_DB_HOST', 'PSQL_DB_PORT', 'PSQL_DB_PASS',
    'PSQL_DB_NAME'
]

def main(args) -> list:
    if args.SQL:
        with open(args.SQL) as input_file:
            args.QUERY = input_file.read()
    elif not args.QUERY:
        print('QUERY or SQL parameter required, both missing.')
        return []
    connection = psycopg2.connect(
        host=args.PSQL_DB_HOST,
        port=args.PSQL_DB_PORT,
        user=args.PSQL_DB_USER,
        password=args.PSQL_DB_PASS,
        database=args.PSQL_DB_NAME
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
