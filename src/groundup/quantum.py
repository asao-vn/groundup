"""Layer 0: electrons and nuclei, solved with quantum mechanics.

This is the only layer where physics is written by hand, and even here it
is not written by us: the electronic Schrödinger equation is solved by
PySCF. For H2 (two electrons) full configuration interaction is used, which
is the *exact* solution of the Schrödinger equation within the chosen basis
set. No empirical parameter enters.

Full CI cost grows exponentially with the number of electrons, so this
module is deliberately limited to hydrogen. Larger systems will need
approximate methods (coupled cluster, DFT) in later milestones.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

import numpy as np


def _pyscf():
    try:
        from pyscf import fci, gto, scf
    except ImportError as exc:  # pragma: no cover - exercised only without pyscf
        raise ImportError("Layer 0 needs PySCF: pip install pyscf") from exc
    return gto, scf, fci


def h2_energy(r_bohr: float, basis: str = "cc-pvtz") -> float:
    """Exact (full CI) ground-state energy of H2 at bond length ``r_bohr``, in Hartree."""
    gto, scf, fci = _pyscf()
    mol = gto.M(
        atom=[["H", (0.0, 0.0, 0.0)], ["H", (0.0, 0.0, float(r_bohr))]],
        unit="Bohr",
        basis=basis,
        verbose=0,
    )
    mf = scf.RHF(mol)
    mf.conv_tol = 1e-11
    mf.kernel()
    if not mf.converged:
        raise RuntimeError(f"RHF reference did not converge at r={r_bohr} bohr")
    energy, _ = fci.FCI(mf).kernel()
    return float(energy)


def h_atom_energy(basis: str = "cc-pvtz") -> float:
    """Energy of an isolated H atom in Hartree.

    With one electron there is no electron correlation, so Hartree-Fock is
    already exact within the basis set.
    """
    gto, scf, _ = _pyscf()
    mol = gto.M(atom=[["H", (0.0, 0.0, 0.0)]], spin=1, basis=basis, verbose=0)
    mf = scf.UHF(mol)
    mf.conv_tol = 1e-11
    return float(mf.kernel())


def h2_potential_curve(
    distances_bohr: Iterable[float],
    basis: str = "cc-pvtz",
    on_point: Callable[[float, float], None] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact H2 energies along a set of bond lengths.

    Returns ``(r, E)`` arrays in bohr and Hartree. ``on_point(r, E)`` is
    called after each point, for progress reporting.
    """
    rs = np.asarray(list(distances_bohr), dtype=float)
    es = np.empty_like(rs)
    for i, r in enumerate(rs):
        es[i] = h2_energy(r, basis)
        if on_point is not None:
            on_point(float(r), float(es[i]))
    return rs, es
