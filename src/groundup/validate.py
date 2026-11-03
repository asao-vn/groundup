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
    factor_tol: float | None = None
    """If set, pass when predicted and reference agree within this factor
    (for quantities such as rate constants, judged on a log scale)."""

    @property
    def rel_error(self) -> float:
        return float((self.predicted - self.reference) / self.reference)

    @property
    def factor(self) -> float:
        ratio = self.predicted / self.reference
        return float(max(ratio, 1.0 / ratio))

    @property
    def passed(self) -> bool:
        if self.factor_tol is not None:
            return bool(self.factor <= self.factor_tol)
        return bool(abs(self.rel_error) <= self.rel_tol)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.update(rel_error=self.rel_error, factor=self.factor, passed=self.passed)
        return d


def _num(x: float) -> str:
    return f"{x:.4g}" if (abs(x) < 1e-2 or abs(x) >= 1e5) else f"{x:.4f}"


def gates_passed(checks: list[Check]) -> bool:
    return all(c.passed for c in checks if c.kind == "gate")


def format_report(checks: list[Check]) -> str:
    rows = [("", "check", "predicted", "reference", "error", "tol")]
    for c in checks:
        if c.kind == "info":
            status = "INFO"
        else:
            status = "PASS" if c.passed else "FAIL"
        if c.factor_tol is not None:
            error, tol = f"x{c.factor:.2f}", f"x{c.factor_tol:.1f}"
        else:
            error, tol = f"{100 * c.rel_error:+.2f}%", f"±{100 * c.rel_tol:.1f}%"
        rows.append(
            (status, c.name, f"{_num(c.predicted)} {c.unit}", f"{_num(c.reference)} {c.unit}", error, tol)
        )
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = ["  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip() for row in rows]
    lines.insert(1, "  ".join("-" * w for w in widths))
    notes = [f"  [{c.name}] {c.note}" for c in checks if c.note]
    if notes:
        lines += ["", "notes:"] + notes
    return "\n".join(lines)
