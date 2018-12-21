import os
import sys

import paramiko

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'SINCE': 'Date of files to find after.',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
}

REQUIRED_ARGS = [
    'SINCE', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def sortable_date(date):
    return date[4:] + date[0:2] + date[2:4]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        since = sortable_date(args.SINCE)
        transport = paramiko.Transport((args.SFTP_HOST, 22))
        transport.connect(username = args.SFTP_USER, password = args.SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.chdir('Outgoing File')
        file_list = sftp.listdir('.')
        new_dates = []
        for file_name in file_list:
            date = ''.join([char for char in file_name if char.isdigit()])
            if sortable_date(date) > since:
                new_dates.append(date)
        return list(set(new_dates))

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Check for new files.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
