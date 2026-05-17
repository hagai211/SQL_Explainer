"""
The analyzer runs every rule against a query and collects the findings.
"""

from sql_explainer.rules import ALL_RULES


def analyze(query):
    """
    Run every registered rule against the query.

    Returns a list of Finding objects (empty list if no problems found).
    """
    findings = []
    for rule in ALL_RULES:
        result = rule(query)
        if result is not None:
            findings.append(result)
    return findings
