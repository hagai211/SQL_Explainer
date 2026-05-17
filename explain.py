"""
SQL Slow Query Explainer - v0.1
A tool that analyzes SQL queries and explains potential performance problems
in plain language.

Usage:
    python explain.py "SELECT * FROM Call_Log ORDER BY 1 DESC"
"""

import sys
import re


# ---------------------------------------------------------------------------
# Each "rule" is a function that looks at the query and returns a problem
# (or None if the query is fine for that rule).
# Adding a new check later = just add a new function and register it below.
# ---------------------------------------------------------------------------

def check_select_star(query):
    """SELECT * returns every column - usually more data than needed."""
    if re.search(r"select\s+\*", query, re.IGNORECASE):
        return {
            "title": "SELECT * returns all columns",
            "why": "Returning every column moves more data than needed and "
                   "can prevent the database from using a covering index.",
            "fix": "List only the columns you actually need.",
        }
    return None


def check_missing_where(query):
    """A query with no WHERE clause may scan the whole table."""
    has_where = re.search(r"\bwhere\b", query, re.IGNORECASE)
    has_from = re.search(r"\bfrom\b", query, re.IGNORECASE)
    if has_from and not has_where:
        return {
            "title": "No WHERE clause",
            "why": "Without a WHERE filter the database may read every row "
                   "in the table (a full table scan).",
            "fix": "Add a WHERE clause to limit the rows, or a TOP/LIMIT "
                   "clause if you only need a sample.",
        }
    return None


def check_leading_wildcard(query):
    """LIKE '%...' cannot use an index - the DB must scan every value."""
    if re.search(r"like\s+'%", query, re.IGNORECASE):
        return {
            "title": "LIKE with a leading wildcard ('%...')",
            "why": "A wildcard at the start of a LIKE pattern means the "
                   "database cannot use an index and must check every row.",
            "fix": "If possible, search for a prefix ('Error%') instead, "
                   "or consider full-text search for substring matching.",
        }
    return None


def check_order_without_limit(query):
    """ORDER BY without TOP/LIMIT sorts the entire result set."""
    has_order = re.search(r"order\s+by", query, re.IGNORECASE)
    has_limit = re.search(r"\b(top|limit)\b", query, re.IGNORECASE)
    if has_order and not has_limit:
        return {
            "title": "ORDER BY without TOP / LIMIT",
            "why": "Sorting the full result set is expensive when you only "
                   "need the first few rows.",
            "fix": "Add TOP (SQL Server) or LIMIT (MySQL/Postgres) if you "
                   "only need part of the sorted result.",
        }
    return None


def check_order_by_position(query):
    """ORDER BY 1 - ordering by column position is fragile and unclear."""
    if re.search(r"order\s+by\s+\d", query, re.IGNORECASE):
        return {
            "title": "ORDER BY column position (e.g. ORDER BY 1)",
            "why": "Ordering by a number is unclear and breaks silently if "
                   "the column list changes. It is not a speed problem by "
                   "itself, but it hides what is really being sorted.",
            "fix": "Order by the explicit column name instead.",
        }
    return None


# Register all rules here. To add a new check: write a function, add it here.
RULES = [
    check_select_star,
    check_missing_where,
    check_leading_wildcard,
    check_order_without_limit,
    check_order_by_position,
]


def analyze(query):
    """Run every rule against the query and collect the problems found."""
    findings = []
    for rule in RULES:
        result = rule(query)
        if result is not None:
            findings.append(result)
    return findings


def print_report(query, findings):
    """Print a human-readable report."""
    print()
    print("Query analyzed:")
    print("  " + query.strip())
    print()

    if not findings:
        print("No obvious issues found by the current rules.")
        print()
        return

    print(f"Found {len(findings)} potential issue(s):")
    print()
    for i, f in enumerate(findings, start=1):
        print(f"{i}. {f['title']}")
        print(f"   Why: {f['why']}")
        print(f"   Fix: {f['fix']}")
        print()


def main():
    if len(sys.argv) < 2:
        print('Usage: python explain.py "YOUR SQL QUERY"')
        sys.exit(1)

    query = sys.argv[1]
    findings = analyze(query)
    print_report(query, findings)


if __name__ == "__main__":
    main()
