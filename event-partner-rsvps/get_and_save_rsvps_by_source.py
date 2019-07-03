import csv
import datetime

import get_results_from_psql_query_with_params
from entry_points import run_from_cli

DESCRIPTION = 'Get RSVPs and save to multiple CSV files by source.'

ARG_DEFINITIONS = {
    'PSQL_DB_USER': 'Username for PostgreSQL connection.',
    'PSQL_DB_HOST': 'Host for PostgreSQL connection.',
    'PSQL_DB_PORT': 'Port for PostgreSQL connection.',
    'PSQL_DB_PASS': 'Pass for PostgreSQL connection.',
    'PSQL_DB_NAME': 'Database name for PostgreSQL.',
    'CAMPAIGN': 'Campaign name.',
    'SOURCES': 'Comma-separated list of sources.'
}

REQUIRED_ARGS = [
    'PSQL_DB_USER', 'PSQL_DB_HOST', 'PSQL_DB_PORT', 'PSQL_DB_PASS',
    'PSQL_DB_NAME', 'CAMPAIGN', 'SOURCES'
]

def main(args) -> list:
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    headers = [
        'email', 'first_name', 'middle_name', 'last_name', 'state',  'city',
        'zip', 'action_datetime', 'role'
    ]
    sources = ["'%s'" % source for source in args.SOURCES.split(',')]
    args.PARAMS = 'campaign=%s&sources=%s' % (args.CAMPAIGN, ','.join(sources))
    args.SQL = 'rsvps_with_source.sql'
    results = get_results_from_psql_query_with_params.main(args)
    results_by_source = {}
    for result in results:
        source = result[0]
        if source not in results_by_source.keys():
            results_by_source[source] = []
        results_by_source[source].append(result[1:])
    files = []
    for source in results_by_source.keys():
        filename = '%s-%s.csv' % (source, today)
        files.append(filename)
        with open(filename, 'w') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=headers)
            writer.writeheader()
            for row in results_by_source.get(source):
                writer.writerow(dict(zip(headers, row)))
    return files

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
