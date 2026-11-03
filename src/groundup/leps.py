"""Joint between layer 0 (quantum) and a reactive three-atom rule.

A reaction needs a rule for three atoms at once: bonds must be able to break
and form. groundup derives one in the LEPS form (London-Eyring-Polanyi-Sato),
built from pieces that already exist:

* the two-atom bond rule derived in M0 (a Morse curve from exact H2), and
* one Sato parameter ``delta``, chosen so that the rule's barrier equals the
  barrier computed exactly in layer 0.

Nothing is typed in from experiment. The residual of the rule against
layer-0 H3 energies, and against the layer-0 triplet H2 curve that LEPS
implies, is recorded as the information this joint loses.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from .bridge import MorseRule
from .provenance import Provenance
from .units import HARTREE_TO_CM1, HARTREE_TO_KCALMOL

_SQRT_FLOOR = 1e-30


@dataclass(frozen=True)
class LEPSRule:
    """LEPS surface for three identical-electron atoms (H, D, T), atomic units.

    Energies are relative to three separated atoms; ``e_atoms`` converts them
    back to absolute layer-0 energies.
    """

    de: float
    a: float
    re: float
    delta: float
    e_atoms: float
    provenance: Provenance | None = None

    # pair terms ----------------------------------------------------------
    def _qj(self, r):
        x = np.exp(-self.a * (np.asarray(r, dtype=float) - self.re))
        d, k = self.delta, self.de / 4.0
        q = k * ((3.0 + d) * x * x - (2.0 + 6.0 * d) * x)
        j = k * ((1.0 + 3.0 * d) * x * x - (6.0 + 2.0 * d) * x)
        dq = -self.a * k * (2.0 * (3.0 + d) * x * x - (2.0 + 6.0 * d) * x)
        dj = -self.a * k * (2.0 * (1.0 + 3.0 * d) * x * x - (6.0 + 2.0 * d) * x)
        return q, j, dq, dj

    def energy(self, r_ab, r_bc, r_ac):
        q1, j1, _, _ = self._qj(r_ab)
        q2, j2, _, _ = self._qj(r_bc)
        q3, j3, _, _ = self._qj(r_ac)
        s = j1 * j1 + j2 * j2 + j3 * j3 - j1 * j2 - j2 * j3 - j3 * j1
        return (q1 + q2 + q3 - np.sqrt(np.maximum(s, 0.0) + _SQRT_FLOOR)) / (1.0 + self.delta)

    def energy_and_distance_gradient(self, r_ab, r_bc, r_ac):
        """Energy and its derivatives with respect to the three distances."""
        q1, j1, dq1, dj1 = self._qj(r_ab)
        q2, j2, dq2, dj2 = self._qj(r_bc)
        q3, j3, dq3, dj3 = self._qj(r_ac)
        s = j1 * j1 + j2 * j2 + j3 * j3 - j1 * j2 - j2 * j3 - j3 * j1
        root = np.sqrt(np.maximum(s, 0.0) + _SQRT_FLOOR)
        scale = 1.0 / (1.0 + self.delta)
        v = (q1 + q2 + q3 - root) * scale
        g1 = (dq1 - (2 * j1 - j2 - j3) * dj1 / (2 * root)) * scale
        g2 = (dq2 - (2 * j2 - j1 - j3) * dj2 / (2 * root)) * scale
        g3 = (dq3 - (2 * j3 - j1 - j2) * dj3 / (2 * root)) * scale
        return v, g1, g2, g3

    def energy_cartesian(self, xyz):
        """Energy for coordinates of shape (..., 3 atoms, 3)."""
        xyz = np.asarray(xyz, dtype=float)
        r_ab = np.linalg.norm(xyz[..., 0, :] - xyz[..., 1, :], axis=-1)
        r_bc = np.linalg.norm(xyz[..., 1, :] - xyz[..., 2, :], axis=-1)
        r_ac = np.linalg.norm(xyz[..., 0, :] - xyz[..., 2, :], axis=-1)
        return self.energy(r_ab, r_bc, r_ac)

    def forces_cartesian(self, xyz):
        """Energy and forces (-gradient) for coordinates of shape (..., 3, 3)."""
        xyz = np.asarray(xyz, dtype=float)
        d_ab = xyz[..., 0, :] - xyz[..., 1, :]
        d_bc = xyz[..., 1, :] - xyz[..., 2, :]
        d_ac = xyz[..., 0, :] - xyz[..., 2, :]
        r_ab = np.linalg.norm(d_ab, axis=-1)
        r_bc = np.linalg.norm(d_bc, axis=-1)
        r_ac = np.linalg.norm(d_ac, axis=-1)
        v, g1, g2, g3 = self.energy_and_distance_gradient(r_ab, r_bc, r_ac)
        u_ab = d_ab / r_ab[..., None]
        u_bc = d_bc / r_bc[..., None]
        u_ac = d_ac / r_ac[..., None]
        f = np.empty_like(xyz)
        f[..., 0, :] = -(g1[..., None] * u_ab + g3[..., None] * u_ac)
        f[..., 1, :] = -(-g1[..., None] * u_ab + g2[..., None] * u_bc)
        f[..., 2, :] = -(-g2[..., None] * u_bc - g3[..., None] * u_ac)
        return v, f

    # derived quantities --------------------------------------------------
    def collinear_symmetric_minimum(self) -> tuple[float, float]:
        """(r, V) of the lowest point on the line r_ab = r_bc in collinear geometry."""
        res = minimize_scalar(lambda r: self.energy(r, r, 2 * r), bounds=(1.0, 3.5), method="bounded",
                              options={"xatol": 1e-9})
        return float(res.x), float(res.fun)

    def barrier(self) -> float:
        """Classical barrier above A + BC (BC at its minimum), Hartree."""
        _, v = self.collinear_symmetric_minimum()
        return v + self.de

    def triplet_curve(self, r):
        """Two-atom triplet energy implied by LEPS, relative to separated atoms."""
        q, j, _, _ = self._qj(r)
        return (q - j) / (1.0 + self.delta)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["provenance"] = self.provenance.to_dict() if self.provenance else None
        d["units"] = {"de": "hartree", "a": "1/bohr", "re": "bohr", "delta": "dimensionless",
                      "e_atoms": "hartree"}
        return d


def derive_leps(
    bond: MorseRule,
    layer0_barrier: float,
    e_atom: float,
    *,
    h3_points: np.ndarray | None = None,
    h3_energies: np.ndarray | None = None,
    triplet_r: np.ndarray | None = None,
    triplet_energies: np.ndarray | None = None,
    source_method: str = "unspecified",
    groundup_version: str = "",
) -> LEPSRule:
    """Derive a LEPS rule from an M0 bond rule and the layer-0 barrier.

    ``delta`` is the single value for which the LEPS barrier equals
    ``layer0_barrier`` (Hartree, above A + BC). ``h3_points`` (rows of
    r1, r2, angle_deg) with absolute ``h3_energies`` and the triplet curve
    are used only to measure what the rule loses.
    """

    def rule(delta: float) -> LEPSRule:
        return LEPSRule(de=bond.de, a=bond.a, re=bond.re, delta=delta, e_atoms=3.0 * e_atom)

    def mismatch(delta: float) -> float:
        return rule(delta).barrier() - layer0_barrier

    lo, hi = -0.3, 0.6
    if mismatch(lo) * mismatch(hi) > 0:
        raise ValueError("no Sato parameter in [-0.3, 0.6] reproduces the layer-0 barrier")
    delta = brentq(mismatch, lo, hi, xtol=1e-12)
    leps = rule(delta)
    r_sad, _ = leps.collinear_symmetric_minimum()

    quality: dict[str, Any] = {"barrier_kcalmol": leps.barrier() * HARTREE_TO_KCALMOL,
                               "saddle_r_bohr": r_sad}
    inputs: dict[str, Any] = {
        "bond_rule": bond.provenance.to_dict() if bond.provenance else None,
        "layer0_barrier_hartree": float(layer0_barrier),
        "e_atom_hartree": float(e_atom),
    }
    if h3_points is not None and h3_energies is not None:
        pts = np.asarray(h3_points, dtype=float)
        r1, r2, ang = pts[:, 0], pts[:, 1], np.radians(pts[:, 2])
        r3 = np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * np.cos(ang))
        resid = leps.energy(r1, r2, r3) + leps.e_atoms - np.asarray(h3_energies, dtype=float)
        quality["h3_rms_residual_kcalmol"] = float(np.sqrt(np.mean(resid**2)) * HARTREE_TO_KCALMOL)
        quality["h3_max_abs_residual_kcalmol"] = float(np.max(np.abs(resid)) * HARTREE_TO_KCALMOL)
        quality["h3_residual_by_point_kcalmol"] = [
            [float(a), float(b), float(c), float(d * HARTREE_TO_KCALMOL)]
            for (a, b, c), d in zip(pts, resid)
        ]
        inputs["n_h3_points"] = len(pts)
    if triplet_r is not None and triplet_energies is not None:
        tr = np.asarray(triplet_r, dtype=float)
        resid_t = leps.triplet_curve(tr) + 2 * e_atom - np.asarray(triplet_energies, dtype=float)
        quality["triplet_residual_by_point_cm1"] = [
            [float(r), float(d * HARTREE_TO_CM1)] for r, d in zip(tr, resid_t)
        ]
    provenance = Provenance(
        source_layer="quantum",
        source_method=source_method,
        procedure=(
            "LEPS surface from the M0 Morse bond rule; Sato parameter solved (brentq) so that the "
            "collinear symmetric saddle energy equals the layer-0 barrier"
        ),
        inputs=inputs,
        quality=quality,
        groundup_version=groundup_version,
    )
    return replace(leps, provenance=provenance)
