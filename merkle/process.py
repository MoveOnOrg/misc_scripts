import os
import sys

import get_last
import check
import decrypt
import download
import import_to_ak
import split
import set_last
import summarize
import notify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'AK_BASEURL': 'ActionKit Base URL.',
    'AK_USER': 'ActionKit API username.',
    'AK_PASSWORD': 'ActionKit API password.',
    'AK_IMPORT_PAGE': 'ActionKit import page name.',
    'CSV': 'CSV file to split.',
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'LAST_RUN_DATE': 'Date of last run.',
    'LAST_RUN_SCRIPT': 'Script name.',
    'PGP_PASS': 'Pass phrase for PGP',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
    'SLACK_WEBHOOK': 'Web hook URL for Slack.',
    'SLACK_CHANNEL': 'Slack channel to send to.',
}

REQUIRED_ARGS = [
    'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE',
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'LAST_RUN_SCRIPT',
    'PGP_PASS', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def date_short_to_iso(date):
    return '20' + date[4:] + '-' + date[:2] + '-' + date[2:4]

def date_iso_to_short(date):
    parts = date.split(' ')[0].split('-')
    return parts[1] + parts[2] + parts[0][2:]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        all_split_files = []
        print('Checking date last run...')
        last_run = date_iso_to_short(get_last.main(args))
        print('Checking for new dates since %s...' % last_run)
        args.SINCE = last_run
        new_dates = check.main(args)
        if len(new_dates) > 0:
            for date in new_dates:
                args.DATE = date
                print('Downloading for %s...' % date)
                files = download.main(args)
                if len(files) > 0:
                    print('Decrypting for %s...' % date)
                    decrypted_files = decrypt.main(args)
                    if len(decrypted_files) > 0:
                        print('Splitting for %s...' % date)
                        for decrypted_file in decrypted_files:
                            args.CSV = decrypted_file
                            split_files = split.main(args)
                            all_split_files = all_split_files + split_files
                        print('Importing for %s...' % date)
                        for split_file in all_split_files:
                            args.CSV = split_file
                            # import_to_ak.main(args)
                            if "donations.csv" in args.CSV:
                                args.TEXT = summarize.main(args)
                                print('Notifying...')
                                notify.main(args)
            iso_dates = sorted([date_short_to_iso(date) for date in new_dates])
            args.LAST_RUN_DATE = iso_dates[-1]
            print('Setting last import date to %s...' % args.LAST_RUN_DATE)
            set_last.main(args)
        else:
            print('No new dates found.')
        return all_split_files

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Process files.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
