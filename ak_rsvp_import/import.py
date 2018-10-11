import csv

from actionkit.api.action import AKActionAPI
from actionkit.api.event import AKEventAPI
import actionkit.utils as ak_utils

import settings

ak_event_api = AKEventAPI(settings)
ak_action_api = AKActionAPI(settings)

with open('rsvps.csv', 'rt') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        source = row.get('source')
        user_id = row.get('user_id')
        event_id = row.get('event_id')
        page_id = row.get('page_id')
        page_name = row.get('page_name')
        akid = ak_utils.generate_akid(settings.AK_SECRET, '.' + user_id)
        ak_event_api.create_signup(user_id, event_id, page_id, fields={
            'source': source
        })
        ak_action_api.create_action(akid, page_name, fields={
            'event_id': event_id,
            'event_signup_ground_rules': 1
        })
