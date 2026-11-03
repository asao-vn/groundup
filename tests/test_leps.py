import numpy as np
import pytest

from groundup.bridge import MorseRule
from groundup.leps import LEPSRule, derive_leps
from groundup.units import HARTREE_TO_KCALMOL

BOND = MorseRule(re=1.4034, de=0.17272, a=1.0364, e_inf=-0.9996)
E_ATOM = -0.4998


def leps(delta=0.13):
    return LEPSRule(de=BOND.de, a=BOND.a, re=BOND.re, delta=delta, e_atoms=3 * E_ATOM)


def test_far_atom_leaves_the_bond_rule():
    r = np.linspace(1.0, 4.0, 13)
    far = 50.0
    v = leps().energy(r, far, r + far)
    singlet = BOND.energy(r) - BOND.e_inf
    assert np.allclose(v, singlet, atol=1e-12)


def test_analytic_forces_match_finite_differences():
    rule = leps()
    xyz = np.array([[0.1, 0.2, -1.9], [0.0, 0.0, 0.0], [0.3, -0.1, 1.6]])
    _, f = rule.forces_cartesian(xyz)
    h = 1e-6
    num = np.empty_like(xyz)
    for i in range(3):
        for d in range(3):
            xp, xm = xyz.copy(), xyz.copy()
            xp[i, d] += h
            xm[i, d] -= h
            num[i, d] = -(rule.energy_cartesian(xp) - rule.energy_cartesian(xm)) / (2 * h)
    assert np.allclose(f, num, atol=1e-7)


def test_sato_parameter_reproduces_the_requested_barrier():
    target = 9.9 / HARTREE_TO_KCALMOL
    rule = derive_leps(BOND, target, E_ATOM, source_method="synthetic")
    assert rule.barrier() == pytest.approx(target, abs=1e-9)
    assert 0.0 < rule.delta < 0.3
    assert rule.provenance.quality["barrier_kcalmol"] == pytest.approx(9.9, abs=1e-6)


def test_loss_is_measured_against_layer0_points():
    rule = derive_leps(
        BOND, 9.9 / HARTREE_TO_KCALMOL, E_ATOM,
        h3_points=np.array([[1.6, 2.4, 180.0], [2.0, 2.0, 90.0]]),
        h3_energies=np.array([-1.66, -1.63]),
    )
    assert len(rule.provenance.quality["h3_residual_by_point_kcalmol"]) == 2
