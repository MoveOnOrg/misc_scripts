import csv
import json

from actionkit.api.base import ActionKitAPI

from entry_points import run_from_cli


DESCRIPTION = 'Erase personally identifying info from ActionKit users.'

ARG_DEFINITIONS = {
    'AK_BASEURL': 'Base URL of ActionKit instance',
    'AK_USER': 'ActionKit username',
    'AK_PASSWORD': 'ActionKit password',
    'IN': 'Input CSV file with user_id column.'
}

REQUIRED_ARGS = [
    'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'IN'
]

def main(args) -> int:

    ak = ActionKitAPI(args)
    count = 0

    with open(args.IN) as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            result = ak.client.post(
                '%s/rest/v1/eraser/' % ak.base_url,
                data=json.dumps({
                    'action_fields': True,
                    'order_user_details': True,
                    'transactional_mailings': True,
                    'user_fields': True,
                    'user_id': row.get('user_id')
                })
            )
            count += 1

    return count


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
