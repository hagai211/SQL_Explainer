# Ideas & Notes

A place to dump ideas so they are not lost. Not a commitment - just a backlog.

## Rules to add later
- Bad joins: missing ON condition (accidental cross join)
- Functions wrapped around indexed columns (e.g. WHERE YEAR(date) = 2026)
- Implicit type conversion (e.g. comparing a string column to a number)
- Too many JOINs
- Missing index hint when filtering on a likely-unindexed column

## Bigger features (later)
- Read SQL Server execution plans (.sqlplan XML files)
- Connect directly to a database and pull live slow queries
- JSON output mode (for integrations)
- Simple web UI

## Two modes (idea from session 1)
- "Why is this slow?"  -> performance
- "Why is this failing?" -> correctness (ambiguous column, missing GROUP BY)

## Open questions
- Which SQL dialect to target first? (SQL Server, since that is what I use daily)
