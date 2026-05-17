"""Rule: detect SELECT * usage."""

import re
from sql_explainer.rules.base import Finding


def check(query):
    """SELECT * returns every column - usually more data than needed."""
    if re.search(r"select\s+\*", query, re.IGNORECASE):
        return Finding(
            title="SELECT * returns all columns",
            why="Returning every column moves more data than needed and "
                "can prevent the database from using a covering index.",
            fix="List only the columns you actually need.",
        )
    return None
