"""Experimental reference data. Every value names its source.

H2, ground state X 1Σg+: NIST Chemistry WebBook, Constants of Diatomic
Molecules (compiled by K. P. Huber and G. H. Herzberg).
"""

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
