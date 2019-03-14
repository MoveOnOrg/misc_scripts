from entry_points import run_from_cli

DESCRIPTION = 'Import file from S3 to Redshift table.'

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
    'S3_PATH': 'Path of file to import.'
}

REQUIRED_ARGS = [
    'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'REDSHIFT_DB', 'REDSHIFT_HOST',
    'REDSHIFT_PASS', 'REDSHIFT_PORT', 'REDSHIFT_TABLE', 'REDSHIFT_USER',
    'S3_BUCKET', 'S3_PATH'
]

def main(args) -> list:
    import psycopg2

    errors = []
    redshift = psycopg2.connect(
        host=args.REDSHIFT_HOST,
        port=args.REDSHIFT_PORT,
        user=args.REDSHIFT_USER,
        password=args.REDSHIFT_PASS,
        database=args.REDSHIFT_DB
    )
    redshift_cursor = redshift.cursor()

    import_sql = (
        f"COPY {args.REDSHIFT_TABLE} "
        f"FROM 's3://{args.S3_BUCKET}/{args.S3_PATH}' "
        f"ACCESS_KEY_ID '{args.AWS_ACCESS_KEY}' "
        f"SECRET_ACCESS_KEY '{args.AWS_SECRET_KEY}' "
        "gzip "
        "delimiter '\\t' NULL AS '\\000' "
        "region as 'us-east-1' "
        "ignoreheader 1 "
        "escape "
        "acceptinvchars "
        "maxerror 100000; "
    )
    try:
        redshift_cursor.execute(import_sql)
        redshift.commit()
    except psycopg2.InternalError as e:
        errors.append(e.pgerror)
    return errors

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
