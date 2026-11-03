"""Layer 1: atoms as classical point masses.

Nothing in this module knows about electrons. The only physics is Newton's
second law, integrated with velocity Verlet, plus whatever bond rule the
bridge hands over. If layer 1 reproduces what layer 0 predicts, the joint
between them works.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class BondRule(Protocol):
    def energy(self, r): ...
    def dvdr(self, r): ...


@dataclass(frozen=True)
class Trajectory:
    t: np.ndarray
    """Time, atomic units."""
    x1: np.ndarray
    x2: np.ndarray
    total_energy: np.ndarray
    """Kinetic + potential energy, Hartree."""

    @property
    def bond_length(self) -> np.ndarray:
        return self.x2 - self.x1


def simulate_diatomic(
    rule: BondRule,
    m1: float,
    m2: float,
    r0: float,
    *,
    dt: float = 1.0,
    n_steps: int = 30000,
) -> Trajectory:
    """Two atoms on a line, released at rest with separation ``r0`` (bohr).

    Masses in electron masses, ``dt`` in atomic time units.
    """
    x1, x2 = 0.0, float(r0)
    v1 = v2 = 0.0
    t = np.empty(n_steps + 1)
    xs1 = np.empty(n_steps + 1)
    xs2 = np.empty(n_steps + 1)
    etot = np.empty(n_steps + 1)

    def force_on_2(r: float) -> float:
        return -float(rule.dvdr(r))

    f2 = force_on_2(x2 - x1)
    for i in range(n_steps + 1):
        r = x2 - x1
        t[i] = i * dt
        xs1[i], xs2[i] = x1, x2
        etot[i] = 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2 + float(rule.energy(r))
        if i == n_steps:
            break
        # velocity Verlet; atom 1 feels the opposite force (Newton's third law)
        v1 += 0.5 * dt * (-f2) / m1
        v2 += 0.5 * dt * f2 / m2
        x1 += dt * v1
        x2 += dt * v2
        f2 = force_on_2(x2 - x1)
        v1 += 0.5 * dt * (-f2) / m1
        v2 += 0.5 * dt * f2 / m2

    return Trajectory(t=t, x1=xs1, x2=xs2, total_energy=etot)


def oscillation_angular_frequency(t: np.ndarray, signal: np.ndarray) -> float:
    """Angular frequency of a periodic signal from its upward mid-line crossings."""
    mid = 0.5 * (signal.max() + signal.min())
    s = signal - mid
    idx = np.nonzero((s[:-1] < 0) & (s[1:] >= 0))[0]
    if idx.size < 3:
        raise ValueError("signal has fewer than 3 full oscillations")
    frac = -s[idx] / (s[idx + 1] - s[idx])
    crossings = t[idx] + frac * (t[idx + 1] - t[idx])
    period = (crossings[-1] - crossings[0]) / (crossings.size - 1)
    return float(2.0 * np.pi / period)
