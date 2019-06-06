import erase
import get_ids
from entry_points import run_from_cli, run_from_lamba


DESCRIPTION = 'Get EU addresses and erase from ActionKit.'

ARG_DEFINITIONS = {
    'AK_BASEURL': 'Base URL of ActionKit instance',
    'AK_USER': 'ActionKit username',
    'AK_PASSWORD': 'ActionKit password',
    'COUNT': 'Number of IDs to get.',
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'DB_TABLE': 'Database table (with schema prefix)',
    'CSV': 'CSV file with user_id column.',
}

REQUIRED_ARGS = [
    'COUNT', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'CSV'
]

def main(args) -> str:
    args.IN = args.CSV
    args.OUT = args.CSV
    get_ids.main(args)
    erase.main(args)
    return args.COUNT


def aws_lambda(event, context) -> str:
    run_from_lamba(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, event)


if __name__ == '__main__':
    run_from_lamba(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, {})
    # run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
