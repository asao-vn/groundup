"""Joint between layer 0 (quantum) and layer 1 (classical atoms).

Layer 1 needs a rule for the force between two atoms. Instead of typing one
in, the rule is *derived* from layer 0: a Morse potential whose three
parameters come from three quantities measured on the layer-0 curve:

* ``re``: position of the minimum (bond length)
* ``k``: curvature at the minimum (sets how fast the bond vibrates)
* ``de``: depth below the exact dissociation limit (two isolated atoms)

The residual of the Morse rule against every layer-0 point is recorded in
the rule's provenance. That residual is the information this joint loses.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

import numpy as np

from .provenance import Provenance
from .units import HARTREE_TO_CM1


@dataclass(frozen=True)
class MorseRule:
    """V(r) = e_inf - de + de * (1 - exp(-a (r - re)))**2, all in atomic units."""

    re: float
    de: float
    a: float
    e_inf: float
    provenance: Provenance | None = None

    def energy(self, r):
        x = np.exp(-self.a * (np.asarray(r, dtype=float) - self.re))
        return self.e_inf - self.de + self.de * (1.0 - x) ** 2

    def dvdr(self, r):
        x = np.exp(-self.a * (np.asarray(r, dtype=float) - self.re))
        return 2.0 * self.de * self.a * (1.0 - x) * x

    # Quantized Morse oscillator (closed form). ``mu`` is the reduced mass in m_e.
    def omega_e(self, mu: float) -> float:
        return self.a * np.sqrt(2.0 * self.de / mu)

    def omega_e_x_e(self, mu: float) -> float:
        w = self.omega_e(mu)
        return w * w / (4.0 * self.de)

    def vib_level(self, n: int, mu: float) -> float:
        """Energy of vibrational level n above the potential minimum."""
        w, wx = self.omega_e(mu), self.omega_e_x_e(mu)
        return w * (n + 0.5) - wx * (n + 0.5) ** 2

    def fundamental(self, mu: float) -> float:
        return self.vib_level(1, mu) - self.vib_level(0, mu)

    def d0(self, mu: float) -> float:
        """Dissociation energy measured from the lowest vibrational level."""
        return self.de - self.vib_level(0, mu)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["provenance"] = self.provenance.to_dict() if self.provenance else None
        d["units"] = {"re": "bohr", "de": "hartree", "a": "1/bohr", "e_inf": "hartree"}
        return d


def _local_minimum(r: np.ndarray, e: np.ndarray, window: float, degree: int):
    i0 = int(np.argmin(e))
    r0 = r[i0]
    mask = np.abs(r - r0) <= window
    if mask.sum() < degree + 1:
        raise ValueError(
            f"need at least {degree + 1} points within {window} bohr of the minimum, got {int(mask.sum())}"
        )
    poly = np.polynomial.Polynomial.fit(r[mask] - r0, e[mask], degree).convert()
    d1, d2 = poly.deriv(1), poly.deriv(2)
    roots = d1.roots()
    roots = roots[np.abs(roots.imag) < 1e-12].real
    roots = roots[(np.abs(roots) <= window) & (d2(roots) > 0)]
    if roots.size == 0:
        raise ValueError("no minimum found in the local fit")
    x = roots[np.argmin(np.abs(roots))]
    local_rms = float(np.sqrt(np.mean((poly(r[mask] - r0) - e[mask]) ** 2)))
    return r0 + x, float(poly(x)), float(d2(x)), int(mask.sum()), local_rms


def derive_morse(
    r_bohr,
    energies_hartree,
    e_dissociation: float,
    *,
    window: float = 0.4,
    degree: int = 6,
    source_layer: str = "quantum",
    source_method: str = "unspecified",
    groundup_version: str = "",
) -> MorseRule:
    """Derive a Morse bond rule from a layer-0 potential curve.

    ``e_dissociation`` is the exact energy of the separated atoms, computed
    in layer 0 (not fitted). The minimum and curvature come from a local
    polynomial fit of degree ``degree`` within ``window`` bohr of the
    lowest sampled point.
    """
    r = np.asarray(r_bohr, dtype=float)
    e = np.asarray(energies_hartree, dtype=float)
    if r.shape != e.shape or r.ndim != 1:
        raise ValueError("r and energies must be 1-D arrays of the same length")

    re, e_min, k, n_local, local_rms = _local_minimum(r, e, window, degree)
    de = e_dissociation - e_min
    if de <= 0:
        raise ValueError("dissociation limit lies below the minimum: no bound state")
    a = float(np.sqrt(k / (2.0 * de)))

    rule = MorseRule(re=float(re), de=float(de), a=a, e_inf=float(e_dissociation))
    resid = rule.energy(r) - e
    provenance = Provenance(
        source_layer=source_layer,
        source_method=source_method,
        procedure=(
            f"degree-{degree} polynomial fit within {window} bohr of the minimum gives re and "
            "curvature; depth from the exact dissociation limit; Morse a = sqrt(k / (2 De))"
        ),
        inputs={
            "n_points": int(r.size),
            "n_points_local_fit": n_local,
            "r_min_bohr": float(r.min()),
            "r_max_bohr": float(r.max()),
            "e_dissociation_hartree": float(e_dissociation),
        },
        quality={
            "local_fit_rms_cm1": local_rms * HARTREE_TO_CM1,
            "morse_rms_residual_cm1": float(np.sqrt(np.mean(resid**2)) * HARTREE_TO_CM1),
            "morse_max_abs_residual_cm1": float(np.max(np.abs(resid)) * HARTREE_TO_CM1),
            "morse_residual_by_point_cm1": [
                [float(ri), float(di * HARTREE_TO_CM1)] for ri, di in zip(r, resid)
            ],
        },
        groundup_version=groundup_version,
    )
    return replace(rule, provenance=provenance)
