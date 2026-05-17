"""Rule: detect a likely implicit type conversion in a WHERE clause."""

import re
from sql_explainer.rules.base import Finding


def check(query):
    # Matches = '123' — a numeric value wrapped in quotes
    if re.search(r"=\s*'\d+'", query, re.IGNORECASE):
        return Finding(
            title="Possible implicit type conversion",
            why="Comparing a numeric column to a quoted string "
                "(e.g. device_id = '12345') forces the database to convert "
                "types at runtime. This can prevent index use and slow the query.",
            fix="Remove the quotes if the column is numeric: "
                "WHERE device_id = 12345.",
        )
    return None
