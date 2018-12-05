import os
import subprocess
import sys

import pexpect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'DATE': 'Date of files to decrypt.',
    'PGP_PASS': 'Pass phrase for PGP'
}

REQUIRED_ARGS = [
    'DATE', 'PGP_PASS'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        subprocess.run(['gpg', '--import', 'merkle-public.key'])

        dm_process = pexpect.spawn(
            'gpg --output MOVEONDM%s.csv --decrypt MOVEONDM%s.csv.pgp' % (
                args.DATE, args.DATE
            )
        )
        dm_process.expect('Enter passphrase:')
        dm_process.sendline(args.PGP_PASS)

        rt_process = pexpect.spawn(
            'gpg --output MOVEONRT%s.csv --decrypt MOVEONRT%s.csv.pgp' % (
                args.DATE, args.DATE
            )
        )
        rt_process.expect('Enter passphrase:')
        rt_process.sendline(args.PGP_PASS)

        return ['MOVEONDM%s.csv' % args.DATE, 'MOVEONRT%s.csv' % args.DATE]

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Decrypt PGP files with GPG.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
