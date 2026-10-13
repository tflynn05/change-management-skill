#!/usr/bin/env python3
"""Validate a change plan produced by the change-management skill.

Checks:
  1. Every required section heading is present, in order.
  2. Every group in the stakeholder map (section 2) has a row in the
     readiness table (section 3).
  3. The judgment-calls list (section 7) is not empty.
  4. Every metric row in section 6 names an owner and a business outcome.
  5. The metrics table has at most eight rows.

Usage: validate_plan.py path/to/plan.md [--legacy]
  --legacy  accept plans written against template v0.1 (no section 0,
            no metrics cap); used for examples/pega-1to1-ops-manager/OUTPUT.md
Exit code 0 when all checks pass, 1 otherwise.
"""
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 0. One-page summary",
    "## 1. The change at a glance",
    "## 2. Stakeholder and resistance map",
    "### Sponsor coalition",
    "### Top three resistance risks",
    "## 3. Readiness assessment",
    "## 4. Project health check",
    "## 5. Communications and training plan",
    "### Sponsor roadmap",
    "### People-manager toolkit",
    "## 6. Adoption metrics",
    "### Definition of adopted",
    "## 7. Risks, assumptions, and judgment calls",
    "### Judgment calls only an insider can make",
]


def section_text(md: str, heading: str, stop_at_level: int) -> str:
    """Return the text under `heading` up to the next heading of the same or higher level."""
    start = md.find(heading)
    if start < 0:
        return ""
    body = md[start + len(heading):]
    pattern = r"^#{1,%d} " % stop_at_level
    m = re.search(pattern, body, flags=re.MULTILINE)
    return body[: m.start()] if m else body


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue  # separator row
        rows.append(cells)
    return rows


def first_column_groups(text: str) -> list[str]:
    rows = table_rows(text)
    if len(rows) < 2:
        return []
    header, *data = rows
    groups = []
    for r in data:
        if r and r[0] and not r[0].lower().startswith(("group", "leader", "metric", "timing", "audience")):
            groups.append(r[0].strip("* "))
    return groups


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


MAX_METRICS = 8


def main(path: str, legacy: bool = False) -> int:
    md = Path(path).read_text(encoding="utf-8")
    problems = []

    # 1. sections present and ordered
    required = [s for s in REQUIRED_SECTIONS if not (legacy and s.startswith("## 0."))]
    last = -1
    for h in required:
        i = md.find(h)
        if i < 0:
            problems.append(f"missing section: {h}")
        elif i < last:
            problems.append(f"section out of order: {h}")
        else:
            last = i

    # 2. groups in stakeholder map have readiness rows
    stake = section_text(md, "## 2. Stakeholder and resistance map", 3)
    ready = section_text(md, "## 3. Readiness assessment", 3)
    stake_groups = first_column_groups(stake)
    ready_groups = [normalize(g) for g in first_column_groups(ready)]
    if not stake_groups:
        problems.append("stakeholder map has no group rows")
    for g in stake_groups:
        n = normalize(g)
        if not any(n in rg or rg in n for rg in ready_groups if rg):
            problems.append(f"group in stakeholder map has no readiness row: {g}")

    # 3. judgment calls not empty
    jc = section_text(md, "### Judgment calls only an insider can make", 3)
    items = [l for l in jc.splitlines() if re.match(r"^\s*(\d+\.|[-*])\s+\S", l)]
    if not items:
        problems.append("judgment-calls list is empty")

    # 4. metrics rows have an owner and a business outcome
    metrics = section_text(md, "### Metrics", 3)
    rows = table_rows(metrics)
    if len(rows) >= 2:
        header = [h.lower() for h in rows[0]]
        try:
            owner_i = next(i for i, h in enumerate(header) if "owner" in h)
            lead_i = next(i for i, h in enumerate(header) if "leads to" in h or "outcome" in h)
        except StopIteration:
            problems.append("metrics table lacks Owner or Leads-to column")
        else:
            for r in rows[1:]:
                if len(r) <= max(owner_i, lead_i):
                    continue
                if not r[owner_i]:
                    problems.append(f"metric without owner: {r[0]}")
                if not r[lead_i]:
                    problems.append(f"metric without business outcome: {r[0]}")
    else:
        problems.append("metrics table has no rows")

    # 5. metrics cap
    if not legacy and len(rows) - 1 > MAX_METRICS:
        problems.append(f"metrics table has {len(rows) - 1} rows; cap is {MAX_METRICS} (pick the vital few)")

    if problems:
        print("FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"PASS: {len(stake_groups)} groups mapped and assessed, {len(items)} judgment calls, {max(len(rows) - 1, 0)} metrics")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], legacy="--legacy" in flags))
