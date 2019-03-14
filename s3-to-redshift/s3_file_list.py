from entry_points import run_from_cli

DESCRIPTION = 'List of files matching S3 bucket path.'

ARG_DEFINITIONS = {
    'AWS_ACCESS_KEY': 'AWS IAM key.',
    'AWS_SECRET_KEY': 'AWS IAM secret.',
    'S3_BUCKET': 'Name of bucket to search.',
    'S3_PREFIX': 'Prefix path to search for files.'
}

REQUIRED_ARGS = ['AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'S3_BUCKET', 'S3_PREFIX']

def main(args) -> list:
    from boto.s3.connection import S3Connection
    conn = S3Connection(args.AWS_ACCESS_KEY, args.AWS_SECRET_KEY)
    bucket = conn.get_bucket(args.S3_BUCKET)
    return [
        key.name.replace(args.S3_PREFIX, '' )
        for key in bucket.list(prefix=args.S3_PREFIX)
    ]


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
