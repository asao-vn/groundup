"""Provenance: the record every derived rule must carry.

The founding rule of groundup is that only the lowest layer is written by
hand. Every rule used by a higher layer is *derived* from the layer below,
and carries a Provenance that says where it came from, how it was derived,
and how much information the derivation lost.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from typing import Any


def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Provenance:
    source_layer: str
    """Layer the rule was derived from, e.g. "quantum"."""

    source_method: str
    """How that layer was computed, e.g. "FCI/cc-pvtz"."""

    procedure: str
    """How the rule was extracted from the source data."""

    inputs: dict[str, Any] = field(default_factory=dict)
    """What went in: number of points, ranges, settings."""

    quality: dict[str, Any] = field(default_factory=dict)
    """What was lost: residuals of the rule against the source data."""

    groundup_version: str = ""
    created_utc: str = field(default_factory=_now_utc)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
