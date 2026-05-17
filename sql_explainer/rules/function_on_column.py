"""Rule: detect a scalar function wrapping a column inside a WHERE clause."""

import re
from sql_explainer.rules.base import Finding

_SCALAR_FUNCTIONS = (
    r"\b(YEAR|MONTH|DAY|UPPER|LOWER|LEN|LEFT|RIGHT|"
    r"SUBSTRING|ISNULL|DATEPART|FORMAT|LTRIM|RTRIM|TRIM)\s*\("
)


def check(query):
    where_match = re.search(r"\bwhere\b", query, re.IGNORECASE)
    if not where_match:
        return None
    where_clause = query[where_match.start():]
    if re.search(_SCALAR_FUNCTIONS, where_clause, re.IGNORECASE):
        return Finding(
            title="Function applied to a column in WHERE",
            why="Wrapping a column in a function (e.g. YEAR(Created_On) or "
                "UPPER(name)) prevents the database from using an index on "
                "that column, forcing a full scan.",
            fix="Rewrite the condition to isolate the bare column. "
                "For example, replace WHERE YEAR(Created_On) = 2026 with "
                "WHERE Created_On >= '2026-01-01' AND Created_On < '2027-01-01'.",
        )
    return None
