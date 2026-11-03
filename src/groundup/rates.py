"""Bridge from a reactive surface to a rate constant: transition state theory.

The rate of A + BC -> AB + C is not typed in. It is derived from the
surface rule alone: the barrier, the shape of the surface at the saddle
(its normal-mode frequencies), the reactant bond, and the masses. Those
enter conventional transition state theory (Eyring 1935), with the
one-term Wigner (1932) correction for tunnelling through the barrier.

Approximations, recorded with the result: harmonic vibrations, rigid
rotors, a linear transition state, no recrossing, and Wigner tunnelling,
which is only reasonable well above room temperature for hydrogen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .leps import LEPSRule
from .units import AU_RATE_TO_CM3_PER_S, HARTREE_TO_CM1, KB_HARTREE_PER_K


def linear_saddle(rule: LEPSRule) -> np.ndarray:
    """Cartesian coordinates (3 atoms x 3) of the collinear symmetric saddle."""
    r, _ = rule.collinear_symmetric_minimum()
    return np.array([[0.0, 0.0, -r], [0.0, 0.0, 0.0], [0.0, 0.0, r]])


def cartesian_hessian(rule: LEPSRule, xyz: np.ndarray, step: float = 1e-4) -> np.ndarray:
    """9 x 9 Hessian from central differences of the analytic forces."""
    x0 = np.asarray(xyz, dtype=float).reshape(9)
    hess = np.empty((9, 9))
    for j in range(9):
        xp, xm = x0.copy(), x0.copy()
        xp[j] += step
        xm[j] -= step
        _, fp = rule.forces_cartesian(xp.reshape(3, 3))
        _, fm = rule.forces_cartesian(xm.reshape(3, 3))
        hess[:, j] = -(fp - fm).reshape(9) / (2 * step)
    return 0.5 * (hess + hess.T)


def linear_normal_modes(rule: LEPSRule, xyz: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """The 4 vibrational angular frequencies of a linear triatomic, a.u.

    Imaginary frequencies are returned as negative numbers. The 5 modes
    closest to zero (3 translations, 2 rotations) are dropped.
    """
    m = np.repeat(np.asarray(masses, dtype=float), 3)
    hmw = cartesian_hessian(rule, xyz) / np.sqrt(np.outer(m, m))
    eig = np.linalg.eigvalsh(hmw)
    vib = eig[np.argsort(np.abs(eig))][5:]
    return np.sort(np.sign(vib) * np.sqrt(np.abs(vib)))


def _q_vib(omega: np.ndarray, kt: float) -> float:
    """Harmonic vibrational partition function, energies measured from the minimum."""
    return float(np.prod(1.0 / (2.0 * np.sinh(np.asarray(omega) / (2.0 * kt)))))


@dataclass(frozen=True)
class TSTResult:
    temperature_k: float
    k_cm3_per_s: float
    kappa_wigner: float
    barrier_hartree: float
    ts_frequencies_cm1: list[float]
    imaginary_frequency_cm1: float
    reactant_frequency_cm1: float
    details: dict[str, Any] = field(default_factory=dict)


def tst_rate(
    rule: LEPSRule,
    masses: tuple[float, float, float],
    temperature_k: float,
    *,
    sigma_reactant: int,
    sigma_ts: int,
    electronic_ratio: float = 1.0,
) -> TSTResult:
    """Conventional TST rate constant for A + BC with a linear A-B-C saddle.

    ``masses`` are (m_A, m_B, m_C) in electron masses. ``sigma_*`` are
    rotational symmetry numbers (2 for a homonuclear diatomic, 1 for an
    asymmetric linear saddle such as D-H-H). ``electronic_ratio`` is
    g_TS / (g_A g_BC); 2 / (2 x 1) = 1 for H3 doublets.
    """
    m_a, m_b, m_c = (float(x) for x in masses)
    kt = KB_HARTREE_PER_K * float(temperature_k)

    xyz = linear_saddle(rule)
    modes = linear_normal_modes(rule, xyz, np.array([m_a, m_b, m_c]))
    if np.count_nonzero(modes < 0) != 1:
        raise ValueError(f"saddle does not have exactly one imaginary mode: {modes}")
    omega_imag = float(-modes[modes < 0][0])
    omega_ts = modes[modes > 0]

    mu_bc = m_b * m_c / (m_b + m_c)
    omega_bc = rule.a * np.sqrt(2.0 * rule.de / mu_bc)
    i_bc = mu_bc * rule.re**2
    z = xyz[:, 2]
    m_vec = np.array([m_a, m_b, m_c])
    z_com = float(np.sum(m_vec * z) / m_vec.sum())
    i_ts = float(np.sum(m_vec * (z - z_com) ** 2))

    mu_rel = m_a * (m_b + m_c) / (m_a + m_b + m_c)
    q_trans = (2.0 * np.pi / (mu_rel * kt)) ** 1.5
    q_rot = (i_ts / i_bc) * (sigma_reactant / sigma_ts)
    q_vib = _q_vib(omega_ts, kt) / _q_vib(np.array([omega_bc]), kt)
    barrier = rule.barrier()
    kappa = 1.0 + (omega_imag / kt) ** 2 / 24.0

    k_au = kappa * kt / (2.0 * np.pi) * q_trans * q_rot * q_vib * electronic_ratio * np.exp(-barrier / kt)
    return TSTResult(
        temperature_k=float(temperature_k),
        k_cm3_per_s=float(k_au * AU_RATE_TO_CM3_PER_S),
        kappa_wigner=float(kappa),
        barrier_hartree=float(barrier),
        ts_frequencies_cm1=[float(w * HARTREE_TO_CM1) for w in omega_ts],
        imaginary_frequency_cm1=omega_imag * HARTREE_TO_CM1,
        reactant_frequency_cm1=float(omega_bc * HARTREE_TO_CM1),
        details={
            "q_trans_ratio_bohr3": float(q_trans),
            "q_rot_ratio": float(q_rot),
            "q_vib_ratio": float(q_vib),
            "i_ts_me_bohr2": i_ts,
            "i_bc_me_bohr2": float(i_bc),
            "sigma_reactant": sigma_reactant,
            "sigma_ts": sigma_ts,
            "electronic_ratio": electronic_ratio,
        },
    )
