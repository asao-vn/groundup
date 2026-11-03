"""Milestone M0: H2 from the ground up.

    layer 0  quantum      exact Schrödinger solution for H2 (full CI)
       |                  -> potential energy curve, nothing empirical
    bridge   derive       Morse bond rule extracted from that curve
       |                  -> with provenance and residuals
    layer 1  classical    two atoms obeying Newton + the derived rule
       |
    validate              every prediction compared with experiment

The point is not H2. The point is the joint: a higher layer that runs only
on rules derived from the layer below, and checks that prove it.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from .. import __version__, reference
from ..bridge import derive_morse
from ..classical import oscillation_angular_frequency, simulate_diatomic
from ..quantum import h2_potential_curve, h_atom_energy
from ..units import AMU_TO_ME, BOHR_TO_ANGSTROM, HARTREE_TO_CM1, HARTREE_TO_EV, MASS_H_AMU
from ..validate import Check, format_report, gates_passed

DEFAULT_DISTANCES: tuple[float, ...] = (
    1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.4, 3.0, 4.0, 5.0, 6.0,
)

MD_DISPLACEMENT_BOHR = 0.01
MD_DT_AU = 1.0
MD_STEPS = 30000


def run(
    basis: str = "cc-pvtz",
    distances: Sequence[float] = DEFAULT_DISTANCES,
    out_path: str | Path | None = None,
    log: Callable[[str], None] = print,
) -> dict[str, Any]:
    started = time.time()
    method = f"FCI/{basis}"

    log(f"[layer 0] H2 solved exactly ({method}) at {len(distances)} bond lengths")
    r, e = h2_potential_curve(
        distances, basis, on_point=lambda ri, ei: log(f"          r = {ri:4.2f} bohr   E = {ei:.8f} Eh")
    )
    e_atom = h_atom_energy(basis)
    e_inf = 2.0 * e_atom
    log(f"          2 x E(H atom) = {e_inf:.8f} Eh  (dissociation limit, exact)")

    log("[bridge ] deriving the bond rule from the layer-0 curve")
    rule = derive_morse(r, e, e_inf, source_method=method, groundup_version=__version__)
    q = rule.provenance.quality
    log(
        f"          Morse re = {rule.re:.4f} bohr, De = {rule.de * HARTREE_TO_EV:.4f} eV, "
        f"a = {rule.a:.4f} /bohr; residual vs layer 0: rms {q['morse_rms_residual_cm1']:.0f} cm-1, "
        f"max {q['morse_max_abs_residual_cm1']:.0f} cm-1"
    )

    m_h = MASS_H_AMU * AMU_TO_ME
    mu = m_h / 2.0
    log(f"[layer 1] two H atoms, Newton + derived rule, {MD_STEPS} steps of {MD_DT_AU} a.u.")
    traj = simulate_diatomic(rule, m_h, m_h, rule.re + MD_DISPLACEMENT_BOHR, dt=MD_DT_AU, n_steps=MD_STEPS)
    w_md = oscillation_angular_frequency(traj.t, traj.bond_length)
    e_vib = traj.total_energy[0] - (rule.e_inf - rule.de)
    drift = float((traj.total_energy.max() - traj.total_energy.min()) / e_vib)
    log(f"          vibration {w_md * HARTREE_TO_CM1:.1f} cm-1, energy drift {drift:.1e} of vibrational energy")

    w_e = rule.omega_e(mu) * HARTREE_TO_CM1
    checks = [
        Check("bond length r_e", rule.re * BOHR_TO_ANGSTROM, reference.H2_RE_ANGSTROM, "Å", 0.01,
              reference.SOURCE_H2),
        Check("harmonic frequency w_e", w_e, reference.H2_OMEGA_E_CM1, "cm-1", 0.02, reference.SOURCE_H2),
        Check("dissociation energy D_0", rule.d0(mu) * HARTREE_TO_EV, reference.H2_D0_EV, "eV", 0.02,
              reference.SOURCE_H2,
              note="D_0 = De - zero-point energy of the quantized derived rule"),
        Check("fundamental G(1)-G(0)", rule.fundamental(mu) * HARTREE_TO_CM1, reference.H2_FUNDAMENTAL_CM1,
              "cm-1", 0.02, reference.SOURCE_H2_FUNDAMENTAL,
              note="levels of the derived Morse rule, quantized in closed form"),
        Check("layer 1 MD freq = layer 0 w_e", w_md * HARTREE_TO_CM1, w_e, "cm-1", 0.002,
              "layer 0, this run",
              note="joint consistency: classical atoms reproduce the curvature they were handed"),
        Check("anharmonicity w_e x_e", rule.omega_e_x_e(mu) * HARTREE_TO_CM1, reference.H2_OMEGA_E_X_E_CM1,
              "cm-1", 0.10, reference.SOURCE_H2, kind="info",
              note="loss in the joint: a 3-parameter Morse shape only approximates the true curve"),
        Check("classical MD freq vs fundamental", w_md * HARTREE_TO_CM1, reference.H2_FUNDAMENTAL_CM1,
              "cm-1", 0.02, reference.SOURCE_H2_FUNDAMENTAL, kind="info",
              note="loss in layer 1: classical nuclei have no zero-point motion, so they vibrate at w_e"),
    ]

    report = format_report(checks)
    ok = gates_passed(checks)
    log("")
    log(report)
    log("")
    log(f"M0 {'PASSED' if ok else 'FAILED'} in {time.time() - started:.0f}s")

    result: dict[str, Any] = {
        "milestone": "M0-H2",
        "groundup_version": __version__,
        "passed": ok,
        "layer0": {
            "method": method,
            "r_bohr": r.tolist(),
            "energy_hartree": e.tolist(),
            "h_atom_energy_hartree": e_atom,
        },
        "derived_rule": {"kind": "morse", **rule.to_dict()},
        "layer1": {
            "dt_au": MD_DT_AU,
            "n_steps": MD_STEPS,
            "initial_displacement_bohr": MD_DISPLACEMENT_BOHR,
            "frequency_cm1": w_md * HARTREE_TO_CM1,
            "energy_drift_fraction": drift,
        },
        "checks": [c.to_dict() for c in checks],
        "reference_url": reference.NIST_H2_URL,
    }
    if out_path is not None:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        log(f"result written to {path}")
    return result


__all__ = ["DEFAULT_DISTANCES", "run"]
