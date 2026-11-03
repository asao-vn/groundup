# M1: the first reaction, D + H2 → HD + H

**Status:** passed. The rate constant derived from exact quantum chemistry
matches shock-tube measurements within a factor of 1.21 at 700–1900 K. The
tolerance was a factor of 2.

M1 is the first milestone where chemistry happens: a bond breaks and a new one
forms. It uses deuterium (D, hydrogen with one extra neutron) because the
reaction D + H2 → HD + H has been measured directly at high temperature
([Michael & Fisher 1990](../references.md#michael1990)), and because it shows
something important: the potential energy surface depends only on electrons
and nuclear charges, not on nuclear masses
([Born & Oppenheimer 1927](../references.md#born1927)). One surface, derived
from exact H3 calculations, serves every isotope. Only the motion sees the
mass.

```
layer 0   quantum     exact H2 (M0), exact H3 near the barrier, exact triplet H2
   │                  → nothing empirical
bridge 1  derive      reactive LEPS rule: the M0 bond rule + one Sato parameter
   │                  fixed by the layer-0 barrier
layer 1   classical   three atoms collide; bonds break and form by themselves
   │
bridge 2  derive      rate constant k(T) from the surface rule alone
   │                  (transition state theory + Wigner tunnelling)
validate              k(T) vs shock-tube measurements
```

## Layer 0: exact H3

H3 has three electrons, so full configuration interaction is still affordable.
It is exact within the cc-pVTZ basis
([Dunning 1989](../references.md#dunning1989)) and is computed with PySCF
([Sun et al. 2020](../references.md#sun2020)), with the spin fixed to the
doublet ground state. Each point takes about half a minute, so layer 0 is kept
small:

- **5 barrier points**: collinear H–H–H with equal bond lengths from 1.65 to
  1.85 bohr. A cubic fit puts the top of the barrier at r = 1.7575 bohr,
  **9.938 kcal/mol** above H + H2.
- **9 loss points**: collinear and bent geometries, used only to measure how
  well the derived rule reproduces layer 0.
- **4 triplet H2 points**: the repulsive partner of the H2 bond, also used only
  to measure loss.

The H2 bond rule is the one derived in [M0](m0-h2.md), recomputed in the same run.

For comparison, the complete-basis-set estimate of this barrier is
9.60 ± 0.02 kcal/mol ([Peterson et al. 1994](../references.md#peterson1994)).
cc-pVTZ therefore puts the barrier 0.34 kcal/mol (3.5%) too high. This is a
layer-0 basis-set error, and it is carried unchanged into every layer above.
It is a comparison, not a gate.

## Bridge 1: a reactive rule from layer 0

A reaction needs a rule for three atoms at once. groundup derives one in the
LEPS form ([London 1929](../references.md#london1929);
[Eyring & Polanyi 1931](../references.md#eyring1931);
[Sato 1955](../references.md#sato1955)). LEPS builds the three-atom energy from
two-atom pieces, here the Morse bond rule from M0, plus one Sato parameter Δ.

Δ is not fitted to experiment. It is the single value for which the rule's
barrier equals the layer-0 barrier, found by root-finding. Result:
**Δ = 0.1301**. Only the barrier height was imposed, yet the rule's saddle
point lands at r = 1.7600 bohr, against 1.7575 bohr in layer 0 (+0.14%).

The joint's losses are measured against the layer-0 points that were *not*
used to set Δ (rule minus layer 0):

| r1 (bohr) | r2 (bohr) | angle | rule − layer 0 (kcal/mol) |
|---|---|---|---|
| 1.40 | 2.20 | 180° | −1.33 |
| 1.40 | 3.00 | 180° | −0.77 |
| 1.50 | 2.00 | 180° | −0.74 |
| 1.60 | 2.40 | 180° | −0.94 |
| 2.00 | 2.00 | 180° | +0.11 |
| 2.40 | 2.40 | 180° | −0.14 |
| 1.76 | 1.76 | 150° | −0.11 |
| 1.76 | 1.76 | 120° | −0.27 |
| 2.00 | 2.00 | 90° | −1.42 |

The rms error is 0.81 kcal/mol and the largest is 1.42 kcal/mol. Near the
symmetric saddle region, including moderate bends, the rule stays within
0.3 kcal/mol. It is about 1 kcal/mol too low in the entrance channel, where one
bond is near the H2 length and the other is stretched, and 1.4 kcal/mol too
low at the strongly bent 90° point.

The triplet H2 curve implied by the rule is its weakest part. At 1.4 bohr it
is 4368 cm⁻¹ (12.5 kcal/mol) too low, and at 2.0 bohr 2875 cm⁻¹ (8.2 kcal/mol)
too low. At 3.0 and 4.0 bohr it is within 524 cm⁻¹. Every residual is stored in
the rule's provenance.

## Layer 1: atoms that react on their own

D is fired head-on at a resting H2 molecule at 100 collision energies from
0.20 to 1.19 eV. The atoms obey only Newton's law and the derived rule. Nobody
tells them to react; each collision ends either with D bouncing back or with
a new D–H bond and a free H atom.

```
collision energy 0.20 → 1.19 eV, one character per 0.01 eV (R = reacted)
.........................RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
```

Every collision below 0.45 eV bounced, and every collision from 0.45 eV up
reacted, 75 of 100. The rule's barrier is 0.431 eV. The head-on collision needs
slightly more, between 0.01 and 0.02 eV, which we read as the cost of hitting
along the line of centres rather than along the reaction path. The worst energy
drift of any trajectory was 1.6 × 10⁻⁴ of its collision energy.

## Bridge 2: from the surface to a rate constant

The thermal rate constant is derived from the surface rule with conventional
transition state theory ([Eyring 1935](../references.md#eyring1935)). It uses
the barrier height, the vibration frequencies at the saddle point (from the
rule's Hessian), the H2 bond, and the masses of D and H. Tunnelling through the
barrier is added with Wigner's leading-order correction
([Wigner 1932](../references.md#wigner1932)).

On the derived rule, the D–H–H saddle point is linear. It has a doubly
degenerate bend at 836 cm⁻¹, a symmetric stretch at 1820 cm⁻¹ and an imaginary
frequency of 1948i cm⁻¹ along the reaction path. The symmetry numbers are 2 for
H2 and 1 for the D–H–H transition state, which accounts for the two equivalent
H atoms. These frequencies come from the rule only and have not yet been
checked against layer 0.

## Validation

The measured rate is k = 3.76 × 10⁻¹⁰ exp(−4985 K / T) cm³ molecule⁻¹ s⁻¹ over
655–1979 K, ±28% ([Michael & Fisher 1990](../references.md#michael1990)).
groundup compares only inside that range. The tolerance, a factor of 2, was
fixed before the first run.

| T (K) | groundup k (cm³/s) | experiment k (cm³/s) | groundup / experiment | Wigner κ | gate |
|---|---|---|---|---|---|
| 700 | 3.69 × 10⁻¹³ | 3.04 × 10⁻¹³ | 1.21 | 1.67 | PASS |
| 1000 | 2.28 × 10⁻¹² | 2.57 × 10⁻¹² | 0.89 | 1.33 | PASS |
| 1500 | 1.22 × 10⁻¹¹ | 1.35 × 10⁻¹¹ | 0.90 | 1.15 | PASS |
| 1900 | 2.83 × 10⁻¹¹ | 2.73 × 10⁻¹¹ | 1.04 | 1.09 | PASS |

Read this agreement with care. It is closer than the approximations deserve on
their own, so some errors must be cancelling. Two that pull in opposite
directions:

- The layer-0 barrier is 0.34 kcal/mol too high. By itself this lowers k by
  about 22% at 700 K and 9% at 1900 K.
- Conventional transition state theory counts every crossing of the saddle as
  reactive. Recrossing is ignored, so it tends to overestimate the rate
  ([Truhlar et al. 1996](../references.md#truhlar1996)).

M1b, which counts trajectories on the same rule, will measure the second of
these directly.

## What these joints lose

- **Bridge 1** reproduces the barrier height exactly by construction. One Sato
  parameter cannot also shape the whole surface: the errors above reach
  1.4 kcal/mol for H3 and 12.5 kcal/mol for triplet H2.
- **Bridge 2** assumes no recrossing of the saddle, harmonic vibrations, rigid
  rotation and a linear transition state
  ([Truhlar et al. 1996](../references.md#truhlar1996)). Wigner's correction is
  valid only when tunnelling is a small effect, which for hydrogen means well
  above room temperature. At 700 K it already multiplies k by 1.67, so the
  lowest temperature is the least trustworthy. At 300 K it would be badly
  wrong, and groundup does not compare there.
- **Layer 1** collisions here are head-on, with an H2 that is not vibrating and
  not rotating. A real H2 always keeps its zero-point vibration. The
  collisions show that the reaction emerges from the rule, but they are not
  yet a thermal average.

## Known limitations and next step

- The barrier from FCI/cc-pVTZ is 9.94 kcal/mol, 0.34 kcal/mol above the
  complete-basis-set estimate. A larger basis would remove most of this
  difference; it has not been run.
- The saddle-point frequencies of the rule have not been compared with layer 0.
- The rate constant comes from transition state theory, not from counting
  trajectories. The next step (M1b) is to count fully three-dimensional,
  thermally sampled trajectories on the same rule, and compare both with
  experiment.

## Reproduce

```bash
.venv/bin/python -m groundup m1 --out results/m1_dh2.json
```

The run takes about 7 minutes: 423 s with 4 worker processes on a shared
8-core machine, mostly spent on the 14 H3 points. The JSON output contains
every layer-0 energy, both derived rules with their provenance, an example
reactive trajectory, the saddle-point data and every check.
