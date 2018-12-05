import os
import sys

import decrypt
import download
import import_to_ak
import split

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
    'DATE': 'Date of files to download.',
    'PGP_PASS': 'Pass phrase for PGP',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
}

REQUIRED_ARGS = [
    'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE',
    'DATE', 'PGP_PASS', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        all_split_files = []
        print('Downloading...')
        files = download.main(args)
        if len(files) > 0:
            print('Decrypting...')
            decrypted_files = decrypt.main(args)
            if len(decrypted_files) > 0:
                print('Splitting...')
                for decrypted_file in decrypted_files:
                    args.CSV = decrypted_file
                    split_files = split.main(args)
                    all_split_files = all_split_files + split_files
                print('Importing...')
                for split_file in all_split_files:
                    args.CSV = split_file
                    import_to_ak.main(args)
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
