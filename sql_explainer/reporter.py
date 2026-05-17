"""
The reporter formats the findings into a human-readable report.

Keeping printing separate from analyzing means we can later add other
output formats (JSON, HTML) without touching the analysis logic.
"""


def build_report(query, findings):
    """Return the report as a string."""
    lines = []
    lines.append("")
    lines.append("Query analyzed:")
    lines.append("  " + query.strip())
    lines.append("")

    if not findings:
        lines.append("No obvious issues found by the current rules.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"Found {len(findings)} potential issue(s):")
    lines.append("")
    for i, f in enumerate(findings, start=1):
        lines.append(f"{i}. {f.title}")
        lines.append(f"   Why: {f.why}")
        lines.append(f"   Fix: {f.fix}")
        lines.append("")

    return "\n".join(lines)


def print_report(query, findings):
    """Print the report to the screen."""
    print(build_report(query, findings))
