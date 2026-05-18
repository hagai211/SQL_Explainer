# SQL Slow Query Explainer

A command-line tool that analyzes a SQL query and explains its performance problems in plain language — no database connection required.

## Why

Slow queries are frustrating to debug. This tool lets you paste any SQL query and immediately see *what* is likely slow and *why*, written in plain English — not execution-plan XML.

## Run with Python

```bash
python explain.py "SELECT * FROM Call_Log ORDER BY 1 DESC"
```

Example output:

```
Query analyzed:
  SELECT * FROM Call_Log ORDER BY 1 DESC

Found 4 potential issue(s):

1. SELECT * returns all columns
   Why: Returning every column moves more data than needed and can prevent
        the database from using a covering index.
   Fix: List only the columns you actually need.

2. No WHERE clause
   Why: Without a WHERE filter the database may read every row in the table
        (a full table scan).
   Fix: Add a WHERE clause to limit the rows.

3. ORDER BY without TOP / LIMIT
   Why: Sorting the full result set is expensive when you only need the first few rows.
   Fix: Add TOP (SQL Server) or LIMIT (MySQL/Postgres).

4. ORDER BY column position (e.g. ORDER BY 1)
   Why: Ordering by a number breaks silently if the column list changes.
   Fix: Order by the explicit column name instead.
```

## Run with Docker

No Python installation needed.

```bash
# Build the image once
docker build -t sql-explainer .

# Run against any query
docker run --rm sql-explainer "SELECT * FROM Call_Log ORDER BY 1 DESC"
```

## Rules (8 checks)

| Rule | What it catches |
|---|---|
| `SELECT *` | Returns more columns than needed, prevents covering indexes |
| No WHERE clause | Full table scan risk |
| Leading wildcard LIKE | `LIKE '%value'` cannot use an index |
| ORDER BY without TOP/LIMIT | Sorts the entire result set unnecessarily |
| ORDER BY column position | `ORDER BY 1` is fragile and unreadable |
| JOIN without ON | Accidental cross join — every row × every row |
| Function on column in WHERE | `YEAR(date) = 2026` prevents index use |
| Possible implicit type conversion | `device_id = '12345'` forces a type cast |

## Run the tests

```bash
python -m pytest tests/
```

## Project layout

```
sql_explainer/      ← core package (analyzer, reporter, rules)
  rules/            ← one file per check, easy to extend
tests/              ← 17 pytest tests, one per rule trigger/skip
examples/           ← sample slow queries to try the tool on
docs/               ← ideas and notes
explain.py          ← CLI entry point
Dockerfile          ← run without installing Python
```

## Roadmap

- Read SQL Server execution plans (`.sqlplan` XML) to catch issues regex can't see
- Read-only database connection — pull and analyze live slow queries automatically
- Natural-language query suggestions — rewrite a slow query, not just flag it
