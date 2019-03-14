from entry_points import run_from_cli
import s3_file_list
import import_s3_file

DESCRIPTION = 'Import all files in S3 directory to Redshift table.'

ARG_DEFINITIONS = {
    'AWS_ACCESS_KEY': 'AWS IAM key.',
    'AWS_SECRET_KEY': 'AWS IAM secret.',
    'REDSHIFT_DB': 'Database name for Redshift connection.',
    'REDSHIFT_HOST': 'Host for Redshift connection.',
    'REDSHIFT_PASS': 'Password for Redshift connection.',
    'REDSHIFT_PORT': 'Port for Redshift connection.',
    'REDSHIFT_TABLE': 'Table to import into.',
    'REDSHIFT_USER': 'User name for Redshift connection.',
    'S3_BUCKET': 'Name of bucket to import from.',
    'S3_PATH': 'Path of file to import.',
    'S3_PREFIX': 'Prefix path to search for files.'
}

REQUIRED_ARGS = [
    'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'REDSHIFT_DB', 'REDSHIFT_HOST',
    'REDSHIFT_PASS', 'REDSHIFT_PORT', 'REDSHIFT_TABLE', 'REDSHIFT_USER',
    'S3_BUCKET', 'S3_PREFIX'
]

def main(args) -> list:
    errors = []
    list = s3_file_list.main(args)
    for file in list:
        args.S3_PATH = args.S3_PREFIX + file
        errors.extend([
            args.S3_PATH + ' : ' + error
            for error in import_s3_file.main(args)
        ])
    return errors

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
