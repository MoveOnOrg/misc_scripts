SELECT es.event_id, es.id AS signup_id, es.page_id
FROM ak_moveon.events_eventsignup es
JOIN ak_moveon.events_event e ON e.id = es.event_id
WHERE es.role = 'host'
AND es.user_id = {{host_id}}
