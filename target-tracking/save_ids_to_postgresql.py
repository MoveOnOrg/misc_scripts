import psycopg2

from entry_points import run_from_cli

DESCRIPTION = 'Save list of IDs to a PostgreSQL table.'

ARG_DEFINITIONS = {
    'PSQL_DB_USER': 'Username for PostgreSQL connection.',
    'PSQL_DB_HOST': 'Host for PostgreSQL connection.',
    'PSQL_DB_PORT': 'Port for PostgreSQL connection.',
    'PSQL_DB_PASS': 'Pass for PostgreSQL connection.',
    'PSQL_DB_NAME': 'Database name for PostgreSQL.',
    'TABLE': 'Table name to insert into.',
    'IDS': 'Comma-separated list of IDs.'
}

REQUIRED_ARGS = [
    'PSQL_DB_USER', 'PSQL_DB_HOST', 'PSQL_DB_PORT', 'PSQL_DB_PASS',
    'PSQL_DB_NAME', 'TABLE', 'IDS'
]

def divide_chunks(l, size):
    for i in range(0, len(l), size):
        yield l[i:i + size]

def main(args) -> list:
    connection = psycopg2.connect(
        host=args.PSQL_DB_HOST,
        port=args.PSQL_DB_PORT,
        user=args.PSQL_DB_USER,
        password=args.PSQL_DB_PASS,
        database=args.PSQL_DB_NAME
    )
    cursor = connection.cursor()
    all_ids = args.IDS.split(',')
    a = 0

    for ids in list(divide_chunks(all_ids, 100000)):
        a += 1
        placeholders = ', '.join(['(%s, GETDATE())'] * len(ids))
        sql = 'INSERT INTO %s (id, queried_at) VALUES %s' % (
            args.TABLE,
            placeholders
        )
        cursor.execute(sql, ids)
        connection.commit()

    return all_ids

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
