"""The parallel layer-0 path must not hang after PySCF has run in the parent.

Regression test: with ``fork`` (the Linux default before Python 3.14) the
workers hung forever once the parent had started PySCF's OpenMP runtime.
"""

import numpy as np
import pytest

pytest.importorskip("pyscf")

from groundup import quantum

POINTS = [(1.75, 1.75, 180.0), (1.4, 3.0, 180.0)]


def test_parallel_h3_after_pyscf_in_parent_matches_serial():
    quantum.h2_potential_curve([1.4], basis="sto-3g")  # start PySCF/OpenMP in this process first
    serial = quantum.h3_energies(POINTS, basis="sto-3g", workers=1)
    parallel = quantum.h3_energies(POINTS, basis="sto-3g", workers=2)
    np.testing.assert_allclose(parallel, serial, rtol=0, atol=1e-10)
