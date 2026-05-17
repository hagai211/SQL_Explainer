"""Rule: detect a missing WHERE clause."""

import re
from sql_explainer.rules.base import Finding


def check(query):
    """A query with no WHERE clause may scan the whole table."""
    has_where = re.search(r"\bwhere\b", query, re.IGNORECASE)
    has_from = re.search(r"\bfrom\b", query, re.IGNORECASE)
    if has_from and not has_where:
        return Finding(
            title="No WHERE clause",
            why="Without a WHERE filter the database may read every row "
                "in the table (a full table scan).",
            fix="Add a WHERE clause to limit the rows, or a TOP/LIMIT "
                "clause if you only need a sample.",
        )
    return None
