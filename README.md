# SQL Slow Query Explainer

A command-line tool that reads a SQL query and explains potential performance problems in plain language — no database connection required.

## Usage

```bash
python explain.py "SELECT * FROM Call_Log ORDER BY 1 DESC"
```

Example output:

```
Query analyzed:
  SELECT * FROM Call_Log ORDER BY 1 DESC

Found 4 potential issue(s):

1. SELECT * returns all columns
   Why: Returning every column moves more data than needed...
   Fix: List only the columns you actually need.

2. No WHERE clause
   Why: Without a WHERE filter the database may read every row...
   ...
```

## Run the tests

```bash
pytest tests/
```

## Project layout

```
sql_explainer/      ← the package (analyzer, reporter, rules)
tests/              ← pytest tests for every rule
examples/           ← sample slow queries to try
docs/               ← ideas and notes
explain.py          ← entry point
```

## Rules implemented

| Rule | What it catches |
|---|---|
| SELECT * | Returns more columns than needed |
| No WHERE clause | Full table scan risk |
| Leading wildcard LIKE | Non-sargable pattern, index skipped |
| ORDER BY without TOP/LIMIT | Sorts entire result set unnecessarily |
| ORDER BY position | Fragile and unreadable column reference |
