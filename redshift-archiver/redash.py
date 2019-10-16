import json
import os
import requests
import time
from pprint import pprint
import urllib3

urllib3.disable_warnings()


"""
Adapted from https://gist.github.com/arikfr/e3e434d8cfd7f331d499ccf351abbff9
Then stolen wholesale from https://github.com/MoveOnOrg/turtle/blob/main/testreport/redash.py
"""


class RedashPoller:

    def __init__(self, base_url, user_api_key, pause_time=3):
        self.base_url = base_url
        self.api_key = user_api_key
        self.pause = pause_time  # seconds to delay


    def poll_job(self, session, job, query_id):
        while job['status'] not in (3, 4):
            poll_url = '{}/api/jobs/{}'.format(self.base_url, job['id'])
            response = session.get(poll_url, verify=False)
            response_json = response.json()
            job = response_json.get('job', {'status': 'Error NO JOB IN RESPONSE: {}'.format(json.dumps(response_json))})
            print('   poll', poll_url, query_id, job['status'], job.get('error'))
            time.sleep(self.pause)

        if job['status'] == 3:  # 3 = completed
            return job['query_result_id']
        elif job['status'] == 4:  # 3 = ERROR
            raise Exception('Redash Query {} failed: {}'.format(query_id, job['error']))


    def get_fresh_query_result(self, query_id, params):
        """
        params = {'p_param': 1243}
        query_id = 1234
        Returns the request response object, so content can be found at response.content
        """
        s = requests.Session()
        s.headers.update({'Authorization': 'Key {}'.format(self.api_key)})

        response = s.post('{}/api/queries/{}/refresh'.format(self.base_url,
                                                             query_id),
                          params=params,
                          verify=False)

        if response.status_code != 200:
            raise Exception('Refresh failed for query {}. {}'.format(query_id, response.text))

        job = response.json()['job']
        print('POLLING JOB', query_id, job['id'])
        result_id = self.poll_job(s, job, query_id)
        if result_id:
            response = s.get('{}/api/queries/{}/results/{}.{}'.format(self.base_url, query_id, result_id, 'csv'),
                             verify=False)
            if response.status_code != 200:
                raise Exception('Failed getting results for query {}. {}'.format(query_id, response.text))
        else:
            raise Exception('Failed getting result {}. {}'.format(query_id, response.text))
        return response