import get_results_from_mysql_query, save_ids_to_postgresql

from entry_points import run_from_cli, run_from_lamba

DESCRIPTION = 'Get IDs from query and save to table.'

ARG_DEFINITIONS = {
    'MYSQL_DB_USER': 'Username for MySQL connection.',
    'MYSQL_DB_HOST': 'Host for MySQL connection.',
    'MYSQL_DB_PORT': 'Port for MySQL connection.',
    'MYSQL_DB_PASS': 'Pass for MySQL connection.',
    'MYSQL_DB_NAME': 'Database name for MySQL.',
    'PSQL_DB_USER': 'Username for PostgreSQL connection.',
    'PSQL_DB_HOST': 'Host for PostgreSQL connection.',
    'PSQL_DB_PORT': 'Port for PostgreSQL connection.',
    'PSQL_DB_PASS': 'Pass for PostgreSQL connection.',
    'PSQL_DB_NAME': 'Database name for PostgreSQL.',
    'QUERY': 'SQL for query.',
    'SQL': 'File containing SQL for query.',
    'TABLE': 'Table name to insert into.',
    'IDS': 'Comma-separated list of IDs.'
}

REQUIRED_ARGS = [
    'MYSQL_DB_USER', 'MYSQL_DB_HOST', 'MYSQL_DB_PORT', 'MYSQL_DB_PASS',
    'MYSQL_DB_NAME', 'PSQL_DB_USER', 'PSQL_DB_HOST', 'PSQL_DB_PORT',
    'PSQL_DB_PASS', 'PSQL_DB_NAME', 'TABLE'
]

def main(args) -> int:
    ids = [
        str(row.get('id'))
        for row in get_results_from_mysql_query.main(args)
    ]
    args.IDS = ','.join(ids)
    save_ids_to_postgresql.main(args)
    return len(ids)


def aws_lambda(event, context) -> str:
    run_from_lamba(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, event)


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
