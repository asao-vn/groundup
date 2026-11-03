import numpy as np
import pytest

from groundup.bridge import MorseRule
from groundup.leps import LEPSRule
from groundup.rates import linear_normal_modes, linear_saddle, tst_rate
from groundup.reactive import collide_collinear, reaction_threshold, relative_energy_drift
from groundup.units import AMU_TO_ME, HARTREE_TO_EV, MASS_D_AMU, MASS_H_AMU

BOND = MorseRule(re=1.4034, de=0.17272, a=1.0364, e_inf=-0.9996)
RULE = LEPSRule(de=BOND.de, a=BOND.a, re=BOND.re, delta=0.13, e_atoms=-1.4994)
M_H, M_D = MASS_H_AMU * AMU_TO_ME, MASS_D_AMU * AMU_TO_ME


def test_saddle_has_one_imaginary_mode_and_a_degenerate_bend():
    modes = linear_normal_modes(RULE, linear_saddle(RULE), np.array([M_D, M_H, M_H]))
    assert np.count_nonzero(modes < 0) == 1
    real = modes[modes > 0]
    assert real.size == 3
    assert real[0] == pytest.approx(real[1], rel=1e-6)


def test_rate_grows_with_temperature_and_tunnelling_fades():
    k = [tst_rate(RULE, (M_D, M_H, M_H), T, sigma_reactant=2, sigma_ts=1) for T in (700, 1400)]
    assert k[1].k_cm3_per_s > k[0].k_cm3_per_s
    assert k[0].kappa_wigner > k[1].kappa_wigner > 1.0


def test_symmetry_numbers_scale_the_rate():
    a = tst_rate(RULE, (M_D, M_H, M_H), 1000, sigma_reactant=2, sigma_ts=1)
    b = tst_rate(RULE, (M_D, M_H, M_H), 1000, sigma_reactant=1, sigma_ts=1)
    assert a.k_cm3_per_s == pytest.approx(2 * b.k_cm3_per_s)


def test_slow_collisions_bounce_fast_ones_react():
    e = np.array([0.15, 1.0]) / HARTREE_TO_EV
    batch = collide_collinear(RULE, (M_D, M_H, M_H), e)
    assert batch.finished.all()
    assert list(batch.reacted) == [False, True]
    assert relative_energy_drift(batch) < 1e-3
    assert reaction_threshold(batch) == pytest.approx(e[1])


def test_no_collision_reacts_below_the_barrier():
    below = np.linspace(0.05, 0.95, 10) * RULE.barrier()
    batch = collide_collinear(RULE, (M_D, M_H, M_H), below)
    assert batch.finished.all()
    assert not batch.reacted.any()
