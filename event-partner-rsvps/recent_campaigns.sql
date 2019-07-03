SELECT id, name FROM (
SELECT c.id, c.name, MAX(e.updated_at) AS last_event_update FROM ak_moveon.events_campaign c
JOIN ak_moveon.events_event e ON e.campaign_id = c.id
WHERE e.status = 'active'
GROUP BY 1, 2
ORDER BY 3 DESC LIMIT 10)
