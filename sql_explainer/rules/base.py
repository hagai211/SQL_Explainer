"""
Shared structure for all rules.

A "Finding" is what a rule returns when it detects a problem.
Every rule is a function that takes a query string and returns
either a Finding or None.
"""

from dataclasses import dataclass


@dataclass
class Finding:
    """One detected problem in a query."""
    title: str   # short name of the problem
    why: str     # plain-language explanation of why it is slow / bad
    fix: str     # what the user should do about it
