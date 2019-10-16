import re

from actionkit.api.event import AKEventAPI

import get_results_from_mysql_query_with_params
from entry_points import run_from_cli


DESCRIPTION = 'Remove and replace an event host on all events.'

ARG_DEFINITIONS = {
    'OLD_HOST_ID': 'ID of host to remove.',
    'NEW_HOST_ID': 'ID of host to add.',
    'AK_BASEURL': 'Base URL of ActionKit instance',
    'AK_USER': 'ActionKit username',
    'AK_PASSWORD': 'ActionKit password',
    'MYSQL_DB_USER': 'Username for MySQL connection.',
    'MYSQL_DB_HOST': 'Host for MySQL connection.',
    'MYSQL_DB_PORT': 'Port for MySQL connection.',
    'MYSQL_DB_PASS': 'Pass for MySQL connection.',
    'MYSQL_DB_NAME': 'Database name for MySQL.'
}

REQUIRED_ARGS = [
    'OLD_HOST_ID', 'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'MYSQL_DB_USER',
    'MYSQL_DB_HOST', 'MYSQL_DB_PORT', 'MYSQL_DB_PASS', 'MYSQL_DB_NAME'
]

def main(args):
    ak = AKEventAPI(args)
    args.PARAMS = 'host_id=%s' % args.OLD_HOST_ID
    args.SQL = 'events_for_host.sql'
    events = get_results_from_mysql_query_with_params.main(args)
    for event in events:
        event_id = event.get('event_id')
        page_id = event.get('page_id')
        signup_id = event.get('signup_id')
        if args.NEW_HOST_ID:
            # Add new host
            new_host_signup = False
            reponse = ak.list_signups(query_params={
                'event': event_id,
                'user_id': args.NEW_HOST_ID,
                '_limit': 100,
                '_offset': 0
            })
            for object in reponse.get('objects'):
                user_id = re.findall(r'/(\d+)/?$', object.get('user'))[0]
                new_host_signup = {
                    'role': object.get('role'),
                    'id': object.get('id')
                }
            if not new_host_signup:
                ak.create_signup(
                    args.NEW_HOST_ID, event_id, page_id,
                    role='host', fields={'source': 'ak-event-merge'}
                )
            elif new_host_signup.get('role') != 'host':
                ak.update_signup(
                    new_host_signup.get('id'), args.NEW_HOST_ID,
                    event_id, page_id, role='host'
                )
        # Remove old host
        ak.update_signup(
            signup_id, args.OLD_HOST_ID, event_id, page_id, status='deleted'
        )

    return events

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
