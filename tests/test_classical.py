import numpy as np
import pytest

from groundup.bridge import MorseRule
from groundup.classical import oscillation_angular_frequency, simulate_diatomic

RULE = MorseRule(re=1.40, de=0.174, a=1.03, e_inf=-1.0)
M_H = 1837.15


def test_small_vibration_matches_harmonic_frequency():
    traj = simulate_diatomic(RULE, M_H, M_H, RULE.re + 0.01, dt=1.0, n_steps=30000)
    w = oscillation_angular_frequency(traj.t, traj.bond_length)
    assert w == pytest.approx(RULE.omega_e(M_H / 2), rel=1e-3)


def test_energy_is_conserved():
    traj = simulate_diatomic(RULE, M_H, M_H, RULE.re + 0.05, dt=1.0, n_steps=20000)
    e_vib = traj.total_energy[0] - (RULE.e_inf - RULE.de)
    assert np.ptp(traj.total_energy) / e_vib < 1e-3


def test_momentum_is_conserved():
    traj = simulate_diatomic(RULE, M_H, 2 * M_H, RULE.re + 0.05, dt=1.0, n_steps=5000)
    centre = (M_H * traj.x1 + 2 * M_H * traj.x2) / (3 * M_H)
    assert np.ptp(centre) < 1e-9


def test_frequency_needs_several_oscillations():
    t = np.linspace(0, 1, 50)
    with pytest.raises(ValueError):
        oscillation_angular_frequency(t, np.sin(2 * np.pi * t))
