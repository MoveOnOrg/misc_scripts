import os
import re
import sys

from actionkit.api.event import AKEventAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'FROM_EVENT': 'ID of event to remove attendees and hosts from',
    'TO_EVENT': 'ID of event to add attendees and hosts to',
    'SIGNUP_PAGE': 'Integer ID of the signup page for TO_EVENT. Be absolutely certain this is the right page ID - RSVP import will fail silently if it is not.',
    'AK_BASEURL': 'Base URL of ActionKit instance',
    'AK_USER': 'ActionKit username',
    'AK_PASS': 'ActionKit password'
}

REQUIRED_ARGS = [
    'FROM_EVENT', 'TO_EVENT', 'SIGNUP_PAGE', 'AK_BASEURL', 'AK_USER', 'AK_PASS'
]

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def main(args):
    ak_settings = {
        'AK_BASEURL': args.AK_BASEURL,
        'AK_USER': args.AK_USER,
        'AK_PASSWORD': args.AK_PASS
    }
    ak = AKEventAPI(Struct(**ak_settings))
    # Get all existing signups on TO event.
    to_signups = {}
    next = False
    offset = 0
    print('Merging event {} into event {}'.format(args.FROM_EVENT, args.TO_EVENT))
    while next is not None:
        print('Loading TO event signups ... %s' % offset)
        reponse = ak.list_signups(query_params={
            'event': args.TO_EVENT,
            '_limit': 100,
            '_offset': offset
        })
        next = reponse.get('meta', {}).get('next', None)
        offset += 100
        for object in reponse.get('objects'):
            user_id = re.findall(r'/(\d+)/?$', object.get('user'))[0]
            to_signups[user_id] = {
                'role': object.get('role'),
                'id': object.get('id')
            }
    # Get hosts FROM event.
    hosts = []
    next = False
    offset = 0
    while next is not None:
        print('Loading hosts ... %s' % offset)
        host_reponse = ak.list_signups(query_params={
            'event': args.FROM_EVENT,
            'role': 'host',
            '_limit': 100,
            '_offset': offset
        })
        next = host_reponse.get('meta', {}).get('next', None)
        offset += 100
        hosts += host_reponse.get('objects')
    # Save hosts TO event.
    for index, host in enumerate(hosts):
        print('Adding hosts ... %s/%s' % (index + 1, len(hosts)))
        user_id = re.findall(r'/(\d+)/?$', host.get('user'))[0]
        if not to_signups.get(user_id, False):
            ak.create_signup(user_id, args.TO_EVENT, args.SIGNUP_PAGE, role='host', fields={'source': 'ak-event-merge'})
        elif to_signups[user_id].get('role') != 'host':
            ak.update_signup(to_signups[user_id].get('id'), user_id, args.TO_EVENT, args.SIGNUP_PAGE, role='host')
    # Get attendees FROM event.
    attendees = []
    next = False
    offset = 0
    while next is not None:
        print('Loading FROM attendees ... %s' % offset)
        attendee_response = ak.list_signups(query_params={
            'event': args.FROM_EVENT,
            'role': 'attendee',
            '_limit': 100,
            '_offset': offset
        })
        next = attendee_response.get('meta', {}).get('next', None)
        offset += 100
        attendees += attendee_response.get('objects')
    # Save attendees TO event.
    for index, attendee in enumerate(attendees):
        print('Adding attendees ... %s/%s' % (index + 1, len(attendees)))
        user_id = re.findall(r'/(\d+)/?$', attendee.get('user'))[0]
        if not to_signups.get(user_id, False):
            ak.create_signup(user_id, args.TO_EVENT, args.SIGNUP_PAGE, role='attendee', fields={'source': 'ak-event-merge'})
    # Cancel FROM event.
    print('Canceling event {}'.format(args.FROM_EVENT))
    ak.update_event_action(args.FROM_EVENT, {
        'event_status': 'cancelled'
    })
    return {
        'attendees': len(attendees),
        'hosts': len(hosts)
    }

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description='Merge one ActionKit event into another.'
    )
    pp = pprint.PrettyPrinter(indent=2)

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pp.pprint(main(args))
