"""Validation: every layer is judged against experiment, not against itself.

A Check compares a predicted number with a reference number. Two kinds:

* ``gate``: must be within tolerance, or the milestone fails.
* ``info``: a known, expected loss, recorded so nobody mistakes it for
  agreement. Hiding what a joint cannot do is worse than failing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Check:
    name: str
    predicted: float
    reference: float
    unit: str
    rel_tol: float
    reference_source: str
    kind: str = "gate"
    note: str = ""

    @property
    def rel_error(self) -> float:
        return float((self.predicted - self.reference) / self.reference)

    @property
    def passed(self) -> bool:
        return bool(abs(self.rel_error) <= self.rel_tol)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.update(rel_error=self.rel_error, passed=self.passed)
        return d


def gates_passed(checks: list[Check]) -> bool:
    return all(c.passed for c in checks if c.kind == "gate")


def format_report(checks: list[Check]) -> str:
    rows = [("", "check", "predicted", "reference", "error", "tol")]
    for c in checks:
        if c.kind == "info":
            status = "INFO"
        else:
            status = "PASS" if c.passed else "FAIL"
        rows.append(
            (
                status,
                c.name,
                f"{c.predicted:.4f} {c.unit}",
                f"{c.reference:.4f} {c.unit}",
                f"{100 * c.rel_error:+.2f}%",
                f"±{100 * c.rel_tol:.1f}%",
            )
        )
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = ["  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip() for row in rows]
    lines.insert(1, "  ".join("-" * w for w in widths))
    notes = [f"  [{c.name}] {c.note}" for c in checks if c.note]
    if notes:
        lines += ["", "notes:"] + notes
    return "\n".join(lines)
