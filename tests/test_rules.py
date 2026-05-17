from sql_explainer.rules import (
    select_star, missing_where, leading_wildcard, order_by,
    missing_join_condition, function_on_column, implicit_conversion,
)
from sql_explainer.analyzer import analyze


# --- select_star ---

def test_select_star_triggers():
    finding = select_star.check("SELECT * FROM users")
    assert finding is not None
    assert finding.title == "SELECT * returns all columns"

def test_select_star_does_not_trigger():
    finding = select_star.check("SELECT id, name FROM users")
    assert finding is None


# --- missing_where ---

def test_missing_where_triggers():
    finding = missing_where.check("SELECT id FROM users")
    assert finding is not None
    assert finding.title == "No WHERE clause"

def test_missing_where_does_not_trigger():
    finding = missing_where.check("SELECT id FROM users WHERE id = 1")
    assert finding is None


# --- leading_wildcard ---

def test_leading_wildcard_triggers():
    finding = leading_wildcard.check("SELECT * FROM logs WHERE msg LIKE '%Error%'")
    assert finding is not None
    assert finding.title == "LIKE with a leading wildcard ('%...')"

def test_leading_wildcard_does_not_trigger():
    finding = leading_wildcard.check("SELECT * FROM logs WHERE msg LIKE 'Error%'")
    assert finding is None


# --- order_by: without limit ---

def test_order_without_limit_triggers():
    finding = order_by.check_order_without_limit("SELECT id FROM users ORDER BY id")
    assert finding is not None
    assert finding.title == "ORDER BY without TOP / LIMIT"

def test_order_without_limit_does_not_trigger():
    finding = order_by.check_order_without_limit("SELECT TOP 10 id FROM users ORDER BY id")
    assert finding is None


# --- order_by: column position ---

def test_order_by_position_triggers():
    finding = order_by.check_order_by_position("SELECT * FROM users ORDER BY 1")
    assert finding is not None
    assert finding.title == "ORDER BY column position (e.g. ORDER BY 1)"

def test_order_by_position_does_not_trigger():
    finding = order_by.check_order_by_position("SELECT * FROM users ORDER BY name")
    assert finding is None


# --- missing_join_condition ---

def test_missing_join_condition_triggers():
    finding = missing_join_condition.check("SELECT * FROM users u JOIN orders o")
    assert finding is not None
    assert finding.title == "JOIN without an ON condition"

def test_missing_join_condition_does_not_trigger():
    finding = missing_join_condition.check(
        "SELECT * FROM users u JOIN orders o ON u.id = o.user_id"
    )
    assert finding is None


# --- function_on_column ---

def test_function_on_column_triggers():
    finding = function_on_column.check(
        "SELECT * FROM Call_Log WHERE YEAR(Created_On) = 2026"
    )
    assert finding is not None
    assert finding.title == "Function applied to a column in WHERE"

def test_function_on_column_does_not_trigger():
    finding = function_on_column.check(
        "SELECT * FROM Call_Log WHERE Created_On >= '2026-01-01'"
    )
    assert finding is None


# --- implicit_conversion ---

def test_implicit_conversion_triggers():
    finding = implicit_conversion.check(
        "SELECT * FROM devices WHERE device_id = '12345'"
    )
    assert finding is not None
    assert finding.title == "Possible implicit type conversion"

def test_implicit_conversion_does_not_trigger():
    finding = implicit_conversion.check(
        "SELECT * FROM devices WHERE device_id = 12345"
    )
    assert finding is None


# --- clean query: zero findings ---

def test_clean_query_produces_no_findings():
    query = "SELECT id, name FROM users WHERE id = 42 ORDER BY name LIMIT 10"
    findings = analyze(query)
    assert findings == []
