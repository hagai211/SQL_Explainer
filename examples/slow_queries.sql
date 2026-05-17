-- Example: full table scan — no filter, returns all columns, sorted by position
SELECT *
FROM Call_Log WITH(NOLOCK)
ORDER BY 1 DESC;

-- Example: blocked by another query holding the table (correctness / locking issue)
SELECT *
FROM Call_Log
WHERE device_id = 12345
ORDER BY 1 DESC;

-- Example: ambiguous column — query fails, not slow (correctness issue)
SELECT device_id
FROM Call_Log cl
JOIN devices d ON d.device_id = cl.device_id
WHERE d.device_number = '12345_q'
ORDER BY Call_ID DESC;

-- Example: non-sargable LIKE — DB must scan every row
SELECT *
FROM action_log_view
WHERE message LIKE '%Error%';

-- Example: ORDER BY on a non-indexed string/date column
SELECT *
FROM Call_Log
WHERE device_id = 12345
ORDER BY Created_On DESC;

SELECT *
FROM Offenders
ORDER BY First_Name DESC;

-- Example: missing GROUP BY (query error)
SELECT department, employee_name, COUNT(*)
FROM employees
GROUP BY department;
