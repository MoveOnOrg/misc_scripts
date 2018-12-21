import os
import sys

import slackweb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'SLACK_WEBHOOK': 'Web hook URL for Slack.',
    'SLACK_CHANNEL': 'Slack channel to send to.',
    'TEXT': 'Text to send.'
}

REQUIRED_ARGS = [
    'SLACK_WEBHOOK', 'SLACK_CHANNEL', 'TEXT'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        slack = slackweb.Slack(url=args.SLACK_WEBHOOK)
        result = slack.notify(text=args.TEXT, channel=args.SLACK_CHANNEL)
        return result

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Send notification.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
