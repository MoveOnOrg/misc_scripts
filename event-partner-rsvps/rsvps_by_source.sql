SET search_path='ak_moveon';

WITH event_rsvps AS (
  SELECT DISTINCT esu.user_id,
                  esu.event_id,
                  a.source
  FROM core_action a
  JOIN core_eventsignupaction esua ON (esua.action_ptr_id = a.id)
  JOIN events_eventsignup esu ON (esua.signup_id = esu.id
                                  AND esu.role = 'attendee'
                                  AND esu.status = 'active')
  JOIN events_event ee ON (ee.id = esu.event_id)
  JOIN events_campaign c ON (ee.campaign_id = c.id)
  WHERE c.name = '{{campaign}}'
  GROUP BY 1, 2,3
)

SELECT SOURCE, count(*)
FROM event_rsvps
WHERE source NOT LIKE 'fb.ads.%'
GROUP BY 1
UNION
SELECT 'TOTAL' AS SOURCE, count(*)
FROM event_rsvps
ORDER BY 2 DESC
