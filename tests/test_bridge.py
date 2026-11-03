import numpy as np
import pytest

from groundup.bridge import MorseRule, derive_morse

TRUE = MorseRule(re=1.40, de=0.174, a=1.03, e_inf=-1.0)


def test_derive_morse_recovers_a_known_curve():
    r = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 3.0, 5.0])
    rule = derive_morse(r, TRUE.energy(r), TRUE.e_inf, source_method="synthetic")
    assert rule.re == pytest.approx(TRUE.re, rel=1e-4)
    assert rule.de == pytest.approx(TRUE.de, rel=1e-4)
    assert rule.a == pytest.approx(TRUE.a, rel=5e-3)


def test_derived_rule_carries_provenance():
    r = np.linspace(1.0, 2.0, 11)
    rule = derive_morse(r, TRUE.energy(r), TRUE.e_inf, source_method="synthetic")
    p = rule.provenance
    assert p is not None
    assert p.source_method == "synthetic"
    assert p.inputs["n_points"] == 11
    assert "morse_rms_residual_cm1" in p.quality
    assert rule.to_dict()["provenance"]["source_layer"] == "quantum"


def test_unbound_curve_is_rejected():
    r = np.linspace(1.0, 2.0, 11)
    with pytest.raises(ValueError, match="no bound state"):
        derive_morse(r, TRUE.energy(r), e_dissociation=-2.0)


def test_morse_levels_closed_form():
    mu = 918.6
    w, wx = TRUE.omega_e(mu), TRUE.omega_e_x_e(mu)
    assert TRUE.fundamental(mu) == pytest.approx(w - 2 * wx)
    assert TRUE.d0(mu) == pytest.approx(TRUE.de - (w / 2 - wx / 4))
