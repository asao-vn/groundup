"""Milestone M1: the first chemical reaction, D + H2 -> HD + H.

    layer 0   quantum     exact H2 (from M0), exact H3 near the barrier,
       |                  exact triplet H2; nothing empirical
    bridge 1  derive      reactive LEPS rule: the M0 bond rule plus one
       |                  Sato parameter fixed by the layer-0 barrier
    layer 1   classical   three atoms collide; bonds break and form by
       |                  themselves under Newton + the derived rule
    bridge 2  derive      rate constant k(T) from the surface rule alone
       |                  (transition state theory + Wigner tunnelling)
    validate              k(T) vs shock-tube measurements (Michael & Fisher 1990)

The surface does not depend on the masses (Born-Oppenheimer), so the rule
derived for H3 serves D + H2 unchanged; only layer 1 and bridge 2 see the
deuterium mass.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from .. import __version__, reference
from ..leps import derive_leps
from ..quantum import h2_triplet_energy, h3_energies
from ..rates import tst_rate
from ..reactive import collide_collinear, reaction_threshold, relative_energy_drift
from ..units import AMU_TO_ME, HARTREE_TO_EV, HARTREE_TO_KCALMOL, MASS_D_AMU, MASS_H_AMU
from ..validate import Check, format_report, gates_passed
from .m0_h2 import derive_h2_bond

SADDLE_SCAN_BOHR = (1.65, 1.70, 1.75, 1.80, 1.85)
"""Collinear symmetric H-H-H geometries bracketing the barrier top."""

LOSS_POINTS = (
    (1.4, 2.2, 180.0),
    (1.4, 3.0, 180.0),
    (1.5, 2.0, 180.0),
    (1.6, 2.4, 180.0),
    (2.0, 2.0, 180.0),
    (2.4, 2.4, 180.0),
    (1.76, 1.76, 150.0),
    (1.76, 1.76, 120.0),
    (2.0, 2.0, 90.0),
)
"""H3 geometries (r1, r2 in bohr, angle in degrees) used only to measure what the rule loses."""

TRIPLET_R_BOHR = (1.4, 2.0, 3.0, 4.0)
RATE_TEMPERATURES_K = (700.0, 1000.0, 1500.0, 1900.0)
"""Inside the measured range of Michael & Fisher (655-1979 K)."""
RATE_FACTOR_TOL = 2.0
"""Chosen before the first run: experiment quotes +-28%, conventional TST is approximate."""
COLLISION_ENERGIES_EV = tuple(np.round(np.arange(0.20, 1.20, 0.01), 3))


def run(
    basis: str = "cc-pvtz",
    out_path: str | Path | None = None,
    workers: int | None = None,
    log: Callable[[str], None] = print,
) -> dict[str, Any]:
    started = time.time()
    method = f"FCI/{basis}"

    # layer 0 + bridge of M0: the H2 bond rule this milestone builds on
    _, _, e_atom, bond = derive_h2_bond(basis, log=log)
    e_h2_min = bond.e_inf - bond.de

    # layer 0: H3 near the barrier, and points for loss accounting
    log(f"[layer 0] H3 solved exactly ({method}): {len(SADDLE_SCAN_BOHR)} barrier points + "
        f"{len(LOSS_POINTS)} loss points")
    points = [(r, r, 180.0) for r in SADDLE_SCAN_BOHR] + list(LOSS_POINTS)
    energies = h3_energies(
        points, basis, workers=workers,
        on_point=lambda p, ei: log(f"          r1 = {p[0]:4.2f}  r2 = {p[1]:4.2f}  angle = {p[2]:5.1f}"
                                   f"   E = {ei:.8f} Eh"),
    )
    scan_e = energies[: len(SADDLE_SCAN_BOHR)]
    scan_r = np.array(SADDLE_SCAN_BOHR)
    poly = np.polynomial.Polynomial.fit(scan_r, scan_e, 3).convert()
    roots = poly.deriv().roots()
    roots = roots[np.abs(roots.imag) < 1e-12].real
    roots = roots[(roots > scan_r.min()) & (roots < scan_r.max()) & (poly.deriv(2)(roots) > 0)]
    if roots.size != 1:
        raise RuntimeError(f"barrier top not bracketed by the scan: {roots}")
    r_sad0 = float(roots[0])
    barrier0 = float(poly(r_sad0)) - (e_h2_min + e_atom)
    log(f"          barrier top at r = {r_sad0:.4f} bohr, {barrier0 * HARTREE_TO_KCALMOL:.3f} kcal/mol "
        "above H + H2")

    log(f"[layer 0] triplet H2 at {len(TRIPLET_R_BOHR)} bond lengths")
    triplet_e = np.array([h2_triplet_energy(r, basis) for r in TRIPLET_R_BOHR])

    # bridge 1: reactive surface rule
    log("[bridge 1] deriving the reactive LEPS rule")
    leps = derive_leps(
        bond, barrier0, e_atom,
        h3_points=np.array(LOSS_POINTS), h3_energies=energies[len(SADDLE_SCAN_BOHR):],
        triplet_r=np.array(TRIPLET_R_BOHR), triplet_energies=triplet_e,
        source_method=method, groundup_version=__version__,
    )
    q = leps.provenance.quality
    r_sad_leps, _ = leps.collinear_symmetric_minimum()
    log(f"          Sato delta = {leps.delta:.5f}; saddle r = {r_sad_leps:.4f} bohr "
        f"(layer 0: {r_sad0:.4f}); H3 residual rms {q['h3_rms_residual_kcalmol']:.2f}, "
        f"max {q['h3_max_abs_residual_kcalmol']:.2f} kcal/mol")

    # layer 1: collisions
    m_h, m_d = MASS_H_AMU * AMU_TO_ME, MASS_D_AMU * AMU_TO_ME
    masses = (m_d, m_h, m_h)
    e_coll = np.array(COLLISION_ENERGIES_EV) / HARTREE_TO_EV
    log(f"[layer 1] {len(e_coll)} head-on D + H2 collisions, Newton + derived rule only")
    batch = collide_collinear(leps, masses, e_coll)
    threshold = reaction_threshold(batch)
    drift_fraction = relative_energy_drift(batch)
    if not batch.finished.all():
        raise RuntimeError("some collisions did not finish; raise max_steps")
    pattern = "".join("R" if x else "." for x in batch.reacted)
    log(f"          reacted (R) by energy 0.20..1.19 eV: {pattern}")
    log(f"          lowest reactive collision energy {threshold * HARTREE_TO_EV:.2f} eV; "
        f"worst energy drift {drift_fraction:.1e} of the collision energy")

    # bridge 2: rate constants
    log("[bridge 2] rate constants from transition state theory on the derived rule")
    rates = [tst_rate(leps, masses, T, sigma_reactant=2, sigma_ts=1) for T in RATE_TEMPERATURES_K]
    r0 = rates[0]
    log(f"          saddle frequencies {', '.join(f'{w:.0f}' for w in r0.ts_frequencies_cm1)} cm-1, "
        f"imaginary {r0.imaginary_frequency_cm1:.0f}i cm-1")

    checks: list[Check] = []
    for res in rates:
        k_exp = reference.d_h2_rate_michael_fisher(res.temperature_k)
        checks.append(
            Check(f"k(D + H2) at {res.temperature_k:.0f} K", res.k_cm3_per_s, k_exp, "cm3/s", 0.0,
                  reference.SOURCE_D_H2_RATE, factor_tol=RATE_FACTOR_TOL,
                  note=f"Wigner tunnelling factor {res.kappa_wigner:.2f}")
        )
    checks.append(
        Check("collinear reaction threshold vs barrier", threshold * HARTREE_TO_EV,
              leps.barrier() * HARTREE_TO_EV, "eV", 0.25, "bridge 1, this run", kind="info",
              note="layer-1 atoms find the barrier on their own; a resting H2 needs a little extra "
                   "energy because the collision is not aimed along the reaction path")
    )
    checks.append(
        Check("saddle bond length, rule vs layer 0", r_sad_leps, r_sad0, "bohr", 0.02, "layer 0, this run",
              kind="info", note="loss in bridge 1: one Sato parameter fixes the barrier height, not its position")
    )

    report = format_report(checks)
    ok = gates_passed(checks)
    log("")
    log(report)
    log("")
    log(f"M1 {'PASSED' if ok else 'FAILED'} in {time.time() - started:.0f}s")

    example = int(np.argmax(batch.reacted))
    result: dict[str, Any] = {
        "milestone": "M1-DH2",
        "groundup_version": __version__,
        "passed": ok,
        "layer0": {
            "method": method,
            "h_atom_energy_hartree": e_atom,
            "h2_min_energy_hartree": e_h2_min,
            "h3_points": [list(p) for p in points],
            "h3_energy_hartree": energies.tolist(),
            "barrier_top_r_bohr": r_sad0,
            "barrier_hartree": barrier0,
            "triplet_r_bohr": list(TRIPLET_R_BOHR),
            "triplet_energy_hartree": triplet_e.tolist(),
        },
        "bond_rule": {"kind": "morse", **bond.to_dict()},
        "reactive_rule": {"kind": "leps", **leps.to_dict()},
        "layer1": {
            "masses_me": list(masses),
            "collision_energy_ev": list(COLLISION_ENERGIES_EV),
            "reacted": batch.reacted.tolist(),
            "threshold_ev": threshold * HARTREE_TO_EV,
            "energy_drift_fraction": drift_fraction,
            "example_reactive": {
                "collision_energy_ev": float(e_coll[example] * HARTREE_TO_EV),
                "t_au": batch.t.tolist(),
                "r_dh_bohr": batch.r_ab[:, example].tolist(),
                "r_hh_bohr": batch.r_bc[:, example].tolist(),
            },
        },
        "rates": [
            {
                "temperature_k": res.temperature_k,
                "k_cm3_per_s": res.k_cm3_per_s,
                "kappa_wigner": res.kappa_wigner,
                "barrier_kcalmol": res.barrier_hartree * HARTREE_TO_KCALMOL,
                "ts_frequencies_cm1": res.ts_frequencies_cm1,
                "imaginary_frequency_cm1": res.imaginary_frequency_cm1,
                "reactant_frequency_cm1": res.reactant_frequency_cm1,
                **res.details,
            }
            for res in rates
        ],
        "checks": [c.to_dict() for c in checks],
        "reference_doi": reference.D_H2_RATE_DOI,
    }
    if out_path is not None:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        log(f"result written to {path}")
    return result
