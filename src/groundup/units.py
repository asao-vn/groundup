"""Physical constants and unit conversions.

Internal unit system everywhere in groundup: Hartree atomic units
(energy in Hartree, length in bohr, mass in electron masses, time in
atomic time units). Conversions happen only at the edges: reports and
comparison with experiment.

Values: CODATA 2018; 1H and 2H atomic masses from AME2020.
"""

HARTREE_TO_EV = 27.211386245988
HARTREE_TO_CM1 = 219474.6313632
BOHR_TO_ANGSTROM = 0.529177210903
ANGSTROM_TO_BOHR = 1.0 / BOHR_TO_ANGSTROM
AMU_TO_ME = 1822.888486209
AU_TIME_TO_FS = 0.024188843265857

MASS_H_AMU = 1.00782503223
HARTREE_TO_KCALMOL = 627.5094740631
KB_HARTREE_PER_K = 3.166811563e-6

MASS_D_AMU = 2.01410177812

BOHR_TO_CM = BOHR_TO_ANGSTROM * 1e-8
AU_TIME_TO_S = AU_TIME_TO_FS * 1e-15
AU_RATE_TO_CM3_PER_S = BOHR_TO_CM**3 / AU_TIME_TO_S
"""Bimolecular rate constant: bohr^3 per atomic time unit -> cm^3 molecule^-1 s^-1."""
