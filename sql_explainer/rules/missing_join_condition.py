"""Rule: detect a JOIN with no ON clause (accidental cross join)."""

import re
from sql_explainer.rules.base import Finding


def check(query):
    has_join = re.search(r"\bjoin\b", query, re.IGNORECASE)
    has_on = re.search(r"\bon\b", query, re.IGNORECASE)
    if has_join and not has_on:
        return Finding(
            title="JOIN without an ON condition",
            why="A JOIN with no ON clause produces a cross join — every row "
                "in the first table is paired with every row in the second. "
                "This is almost always unintentional and extremely expensive.",
            fix="Add an ON clause to specify the join key, "
                "e.g. JOIN orders ON users.id = orders.user_id.",
        )
    return None
