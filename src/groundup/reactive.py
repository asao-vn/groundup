"""Layer 1 for reactions: three classical atoms on a derived reactive surface.

The atoms only obey Newton's law and the forces of the derived LEPS rule.
Nothing tells them whether to react. In a collinear collision A + BC, either
A bounces off (no reaction) or a new A-B bond forms while B-C breaks and C
flies away. Which one happens is decided by the dynamics alone.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .leps import LEPSRule


@dataclass(frozen=True)
class CollinearBatch:
    collision_energy: np.ndarray
    """Hartree, one per trajectory."""
    reacted: np.ndarray
    """True where A-B formed and C left."""
    finished: np.ndarray
    energy_drift: np.ndarray
    """Largest |E(t) - E(0)| along each trajectory, Hartree."""
    t: np.ndarray
    r_ab: np.ndarray
    """Bond lengths over time, shape (n_steps_saved, n_trajectories)."""
    r_bc: np.ndarray


def collide_collinear(
    rule: LEPSRule,
    masses: tuple[float, float, float],
    collision_energies,
    *,
    r_start: float = 9.0,
    r_bc0: float | None = None,
    dt: float = 2.0,
    max_steps: int = 20000,
    save_every: int = 10,
) -> CollinearBatch:
    """Fire A at a resting BC molecule, head on, at each collision energy.

    BC starts at its bond length with no vibration; A starts ``r_start`` bohr
    from B. Each trajectory ends when one fragment has separated beyond
    ``r_start + 1`` bohr.
    """
    e = np.atleast_1d(np.asarray(collision_energies, dtype=float))
    n = e.size
    m = np.array(masses, dtype=float)
    m_tot = m.sum()
    mu = m[0] * (m[1] + m[2]) / m_tot
    v_rel = np.sqrt(2.0 * e / mu)
    r_bc0 = rule.re if r_bc0 is None else r_bc0

    x = np.zeros((n, 3, 3))
    x[:, 0, 2] = -r_start
    x[:, 2, 2] = r_bc0
    v = np.zeros((n, 3, 3))
    v[:, 0, 2] = v_rel * (m[1] + m[2]) / m_tot
    v[:, 1, 2] = -v_rel * m[0] / m_tot
    v[:, 2, 2] = -v_rel * m[0] / m_tot

    pot, f = rule.forces_cartesian(x)
    e0 = 0.5 * np.einsum("i,nid,nid->n", m, v, v) + pot
    drift = np.zeros(n)
    done = np.zeros(n, dtype=bool)
    reacted = np.zeros(n, dtype=bool)
    ts, rabs, rbcs = [], [], []
    inv_m = (1.0 / m)[None, :, None]

    for step in range(max_steps):
        if step % save_every == 0:
            ts.append(step * dt)
            rabs.append(np.abs(x[:, 1, 2] - x[:, 0, 2]))
            rbcs.append(np.abs(x[:, 2, 2] - x[:, 1, 2]))
        active = ~done
        v[active] += 0.5 * dt * f[active] * inv_m
        x[active] += dt * v[active]
        pot_new, f_new = rule.forces_cartesian(x[active])
        f[active] = f_new
        v[active] += 0.5 * dt * f[active] * inv_m
        e_now = 0.5 * np.einsum("i,nid,nid->n", m, v[active], v[active]) + pot_new
        drift[active] = np.maximum(drift[active], np.abs(e_now - e0[active]))

        r_ab = np.abs(x[:, 1, 2] - x[:, 0, 2])
        r_bc = np.abs(x[:, 2, 2] - x[:, 1, 2])
        newly_reacted = active & (r_bc > r_start + 1.0) & (r_ab < r_bc)
        newly_bounced = active & (r_ab > r_start + 1.0) & (r_bc < r_ab)
        reacted |= newly_reacted
        done |= newly_reacted | newly_bounced
        if done.all():
            break

    return CollinearBatch(
        collision_energy=e,
        reacted=reacted,
        finished=done,
        energy_drift=drift,
        t=np.array(ts),
        r_ab=np.array(rabs),
        r_bc=np.array(rbcs),
    )


def relative_energy_drift(batch: CollinearBatch) -> float:
    """Worst energy drift of any trajectory, as a fraction of its collision energy."""
    return float(np.max(batch.energy_drift / batch.collision_energy))


def reaction_threshold(batch: CollinearBatch) -> float | None:
    """Lowest collision energy (Hartree) at which the collinear reaction happened."""
    hits = batch.collision_energy[batch.reacted & batch.finished]
    return float(hits.min()) if hits.size else None
