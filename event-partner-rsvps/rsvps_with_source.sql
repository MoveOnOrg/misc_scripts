SET search_path = 'ak_moveon';

SELECT a.source,
       u.email,
       u.first_name,
       u.middle_name,
       u.last_name,
       u.state,
       u.city,
       u.zip,
       MIN(a.created_at) AS action_datetime,
       MAX(s.role) AS role
FROM core_user u
JOIN events_eventsignup s ON s.user_id = u.id
JOIN events_event e ON e.id = s.event_id
JOIN events_campaign c ON c.id = e.campaign_id
LEFT JOIN core_action a ON (a.page_id = s.page_id
                            AND a.user_id = u.id)
WHERE c.name = '{{campaign}}'
  AND u.email != 'supportcorps-event-host@moveon.org'
  AND a.source IN ({{sources}})
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8
