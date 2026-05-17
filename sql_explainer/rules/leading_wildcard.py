"""Rule: detect LIKE with a leading wildcard."""

import re
from sql_explainer.rules.base import Finding


def check(query):
    """LIKE '%...' cannot use an index - the DB must scan every value."""
    if re.search(r"like\s+'%", query, re.IGNORECASE):
        return Finding(
            title="LIKE with a leading wildcard ('%...')",
            why="A wildcard at the start of a LIKE pattern means the "
                "database cannot use an index and must check every row.",
            fix="If possible, search for a prefix ('Error%') instead, "
                "or consider full-text search for substring matching.",
        )
    return None
