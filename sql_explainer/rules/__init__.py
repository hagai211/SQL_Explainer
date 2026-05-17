"""
Rules package.

ALL_RULES is the master list of every check the tool runs.
To add a new rule:
  1. Create a new file in this folder with a check() function
  2. Import it here
  3. Add it to ALL_RULES
Nothing else in the project needs to change.
"""

from sql_explainer.rules import select_star
from sql_explainer.rules import missing_where
from sql_explainer.rules import leading_wildcard
from sql_explainer.rules import order_by
from sql_explainer.rules import missing_join_condition
from sql_explainer.rules import function_on_column
from sql_explainer.rules import implicit_conversion

ALL_RULES = [
    select_star.check,
    missing_where.check,
    leading_wildcard.check,
    order_by.check_order_without_limit,
    order_by.check_order_by_position,
    missing_join_condition.check,
    function_on_column.check,
    implicit_conversion.check,
]
