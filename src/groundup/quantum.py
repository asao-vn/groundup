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

import multiprocessing
import os
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import ProcessPoolExecutor

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


def h2_triplet_energy(r_bohr: float, basis: str = "cc-pvtz") -> float:
    """Exact (full CI) energy of the lowest triplet state of H2, in Hartree.

    The triplet is repulsive at every bond length; it is the "anti-bonding"
    partner of the ground state and enters the H3 surface through the bridge.
    """
    gto, scf, fci = _pyscf()
    mol = gto.M(
        atom=[["H", (0.0, 0.0, 0.0)], ["H", (0.0, 0.0, float(r_bohr))]],
        unit="Bohr",
        basis=basis,
        spin=2,
        verbose=0,
    )
    mf = scf.ROHF(mol)
    mf.conv_tol = 1e-11
    mf.kernel()
    energy, _ = fci.FCI(mf).kernel()
    return float(energy)


def h3_geometry(r1_bohr: float, r2_bohr: float, angle_deg: float = 180.0) -> list:
    """Atoms A-B-C with |AB| = r1, |BC| = r2 and angle ABC (180 = collinear)."""
    theta = np.radians(angle_deg)
    return [
        ["H", (0.0, 0.0, -float(r1_bohr))],
        ["H", (0.0, 0.0, 0.0)],
        ["H", (float(r2_bohr) * np.sin(theta), 0.0, -float(r2_bohr) * np.cos(theta))],
    ]


def h3_energy(r1_bohr: float, r2_bohr: float, angle_deg: float = 180.0, basis: str = "cc-pvtz") -> float:
    """Exact (full CI) ground-state doublet energy of H3, in Hartree.

    Three electrons in the full orbital space of the basis. Full CI does not
    depend on the orbitals it starts from, so the ROHF step only supplies an
    orthonormal basis; spin is pinned to the doublet (S = 1/2).
    """
    gto, scf, fci = _pyscf()
    mol = gto.M(atom=h3_geometry(r1_bohr, r2_bohr, angle_deg), unit="Bohr", basis=basis, spin=1, verbose=0)
    mf = scf.ROHF(mol)
    mf.conv_tol = 1e-10
    mf.kernel()
    solver = fci.FCI(mf)
    fci.addons.fix_spin_(solver, ss=0.75)
    energy, _ = solver.kernel()
    return float(energy)


def _h3_point(args: tuple) -> float:
    r1, r2, angle, basis = args
    return h3_energy(r1, r2, angle, basis)


def h3_energies(
    points: Sequence[tuple[float, float, float]],
    basis: str = "cc-pvtz",
    workers: int | None = None,
    on_point: Callable[[tuple[float, float, float], float], None] | None = None,
) -> np.ndarray:
    """Full-CI H3 energies for ``(r1, r2, angle_deg)`` points, run in parallel processes.

    Each point is independent, so they are spread over ``workers`` processes
    (default: half the CPU count, at most 4). Results keep the input order.

    Workers are always started with ``spawn``. ``fork`` (the Linux default
    before Python 3.14) copies a parent whose OpenMP runtime PySCF has already
    started, and the children then hang forever. Like any ``spawn`` user, a
    script that calls this must guard its entry point with
    ``if __name__ == "__main__":``.
    """
    if workers is None:
        workers = max(1, min(4, (os.cpu_count() or 2) // 2))
    jobs = [(float(r1), float(r2), float(ang), basis) for r1, r2, ang in points]
    out = np.empty(len(jobs))
    if workers == 1:
        results = map(_h3_point, jobs)
    else:
        pool = ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context("spawn"))
        results = pool.map(_h3_point, jobs)
    try:
        for i, e in enumerate(results):
            out[i] = e
            if on_point is not None:
                on_point(tuple(jobs[i][:3]), float(e))
    finally:
        if workers != 1:
            pool.shutdown()
    return out


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
