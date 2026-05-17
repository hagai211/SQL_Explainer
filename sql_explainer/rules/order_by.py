"""Rules related to ORDER BY clauses."""

import re
from sql_explainer.rules.base import Finding


def check_order_without_limit(query):
    """ORDER BY without TOP/LIMIT sorts the entire result set."""
    has_order = re.search(r"order\s+by", query, re.IGNORECASE)
    has_limit = re.search(r"\b(top|limit)\b", query, re.IGNORECASE)
    if has_order and not has_limit:
        return Finding(
            title="ORDER BY without TOP / LIMIT",
            why="Sorting the full result set is expensive when you only "
                "need the first few rows.",
            fix="Add TOP (SQL Server) or LIMIT (MySQL/Postgres) if you "
                "only need part of the sorted result.",
        )
    return None


def check_order_by_position(query):
    """ORDER BY 1 - ordering by column position is fragile and unclear."""
    if re.search(r"order\s+by\s+\d", query, re.IGNORECASE):
        return Finding(
            title="ORDER BY column position (e.g. ORDER BY 1)",
            why="Ordering by a number is unclear and breaks silently if "
                "the column list changes.",
            fix="Order by the explicit column name instead.",
        )
    return None
