"""Physical constants and unit conversions.

Internal unit system everywhere in groundup: Hartree atomic units
(energy in Hartree, length in bohr, mass in electron masses, time in
atomic time units). Conversions happen only at the edges: reports and
comparison with experiment.

Values: CODATA 2018; 1H atomic mass from AME2020.
"""

HARTREE_TO_EV = 27.211386245988
HARTREE_TO_CM1 = 219474.6313632
BOHR_TO_ANGSTROM = 0.529177210903
ANGSTROM_TO_BOHR = 1.0 / BOHR_TO_ANGSTROM
AMU_TO_ME = 1822.888486209
AU_TIME_TO_FS = 0.024188843265857

MASS_H_AMU = 1.00782503223
