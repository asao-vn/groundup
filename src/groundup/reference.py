"""Experimental reference data. Every value names its source.

H2, ground state X 1Σg+: NIST Chemistry WebBook, Constants of Diatomic
Molecules (compiled by K. P. Huber and G. H. Herzberg).

D + H2 -> HD + H thermal rate constant: Michael & Fisher (1990), flash
photolysis-shock tube measurements, Arrhenius expression from the abstract.
"""

import math

from .units import HARTREE_TO_CM1, HARTREE_TO_EV

_NIST_H2 = "NIST Chemistry WebBook, H2 X 1Σg+ (Huber & Herzberg)"
NIST_H2_URL = "https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=1000"

H2_RE_ANGSTROM = 0.74144
H2_OMEGA_E_CM1 = 4401.213
H2_OMEGA_E_X_E_CM1 = 121.336
H2_D0_CM1 = 36118.3
H2_D0_EV = H2_D0_CM1 / HARTREE_TO_CM1 * HARTREE_TO_EV
# G(1) - G(0) from the tabulated two-term expansion: omega_e - 2 omega_e x_e
H2_FUNDAMENTAL_CM1 = H2_OMEGA_E_CM1 - 2.0 * H2_OMEGA_E_X_E_CM1

SOURCE_H2 = _NIST_H2
SOURCE_H2_FUNDAMENTAL = _NIST_H2 + ", G(1)-G(0) = ωe - 2ωexe"

# D + H2 -> HD + H, flash photolysis-shock tube, 655-1979 K, +-28%.
# J. V. Michael, J. R. Fisher, J. Phys. Chem. 94, 3318-3323 (1990); expression from the abstract.
D_H2_RATE_DOI = "10.1021/j100371a022"
D_H2_RATE_A_CM3_PER_S = 3.76e-10
D_H2_RATE_EA_K = 4985.0
D_H2_RATE_T_RANGE_K = (655.0, 1979.0)
SOURCE_D_H2_RATE = "Michael & Fisher 1990, J. Phys. Chem. 94, 3318 (shock tube, 655-1979 K)"


def d_h2_rate_michael_fisher(temperature_k: float) -> float:
    """Measured k(D + H2 -> HD + H) in cm^3 molecule^-1 s^-1, inside the measured range only."""
    lo, hi = D_H2_RATE_T_RANGE_K
    if not lo <= temperature_k <= hi:
        raise ValueError(f"{temperature_k} K is outside the measured range {lo}-{hi} K")
    return D_H2_RATE_A_CM3_PER_S * math.exp(-D_H2_RATE_EA_K / temperature_k)
